# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for processing cross validation strategies for datasets."""
import numpy as np
import pandas as pd

from sklearn import model_selection


class _CVSplits:

    def __init__(self, X, y, seed=123, frac_test=None,
                 frac_valid=None, CV=None,
                 cv_splits_indices=None):
        """
        Initialize the CV splits class and create CV split indices
        :param X: input data
        :param y: label
        :param seed: random seed to use in spliting data.
        :param frac_test: Fraction of input data to be used as test set
        :param frac_valid: Fraction of input data to be used as validation set
        :param CV: cross validation #
        :param cv_splits_indices: list of np arrays of train, valid indexes
        """
        # Caching the configuration for CV splits
        self._frac_test = frac_test
        self._frac_valid = frac_valid
        self._CV = CV
        self._cv_splits_indices = cv_splits_indices

        # Cache the type of cross validation split
        self._cv_split_type = None

        # These will be populated in case percentage of test
        # and validation sets are provided
        self._train_indices = None
        self._valid_indices = None
        self._test_indices = None

        # Featurized data for train, test and validation sets
        self._featurized_train_test_valid_chunks = None

        # CV splits indices in case of custom CV splits, Monte Carlo split
        # and K-folds split.
        self._CV_splits = None

        # Caching the featurized data for CV splits if any
        self._featurized_cv_splits = None

        # Validate the CV parameters
        self._validate_cv_parameters(X, frac_test,
                                     frac_valid, CV, cv_splits_indices)

        # determine the type of cross validation
        self._cv_split_type = self._find_cv_split_type(frac_test,
                                                       frac_valid, CV,
                                                       cv_splits_indices)

        # Create CV splits or train, test and validation sets
        self._create_cv_splits(X, frac_test,
                               frac_valid, CV, cv_splits_indices, seed)

    def get_fraction_validation_size(self):
        """
        Return the fraction of data to be used as validation set
        """
        return self._frac_valid

    def get_fraction_test_size(self):
        """
        Return the fraction of data to be used as test set
        """
        return self._frac_test

    def get_num_k_folds(self):
        """
        Return the number of k-folds
        """
        return self._CV

    def get_custom_split_indices(self):
        """
        Return the custom split indices
        """
        return self._cv_splits_indices

    def get_cv_split_type(self):
        """
        Return the type of cross validation split
        """
        return self._cv_split_type

    def get_cv_split_indices(self):
        """
        Return a list of tuple (train, valid) is a cross validation
        scenario
        """
        return self._CV_splits

    def get_featurized_cv_split_data(self):
        """
        Return a list of featurized cross validation data
        """
        return self._featurized_cv_splits

    def get_train_test_valid_indices(self):
        """
        Returns train, test and validation indices
        """
        return self._train_indices, self._test_indices, self._valid_indices

    def get_featurized_train_test_valid_data(self):
        """
        Returns featurized train, test and validation data
        """
        featurized_train_chunk = \
            {'X': self._featurized_train_test_valid_chunks.
             _X_train_transformed,
             'y': self._featurized_train_test_valid_chunks.
             _y_train,
             'sample_weight': self._featurized_train_test_valid_chunks.
             _sample_wt_train}
        featurized_test_chunk = \
            {'X': self._featurized_train_test_valid_chunks.
             _X_test_transformed,
             'y': self._featurized_train_test_valid_chunks.
             _y_test,
             'sample_weight': self._featurized_train_test_valid_chunks.
             _sample_wt_test}
        featurized_valid_chunk = \
            {'X': self._featurized_train_test_valid_chunks.
             _X_valid_transformed,
             'y': self._featurized_train_test_valid_chunks.
             _y_valid,
             'sample_weight': self._featurized_train_test_valid_chunks
             ._sample_wt_valid}
        return featurized_train_chunk, featurized_test_chunk, \
            featurized_valid_chunk

    def _find_cv_split_type(self, frac_test, frac_valid,
                            CV, cv_splits_indices):
        """
        Find the type of cross validation split
        :param frac_test: Fraction of input data to be used as test set
        :param frac_valid: Fraction of input data to be used as validation set
        :param CV: cross validation #
        :param cv_splits_indices: list of np arrays of train, valid indexes
        :return: Type of cross validation training
        """
        if CV is None:
            CV = 0

        if cv_splits_indices is not None:
            return _CVType.CustomCrossValitionSplit
        elif CV > 0 and not frac_valid:
            return _CVType.KFoldCrossValitionSplit
        elif CV > 0 and frac_valid:
            return _CVType.MonteCarloCrossValitionSplit
        elif frac_valid and frac_test:
            return _CVType.TrainTestValitionPercSplit
        elif frac_valid:
            return _CVType.TrainValitionPercSplit
        else:
            raise ValueError("Not a valid cross validation scenario")

    def _validate_cv_parameters(self, X, frac_test, frac_valid, CV,
                                cv_splits_indices):
        """
        Validate the cross validation parameters
        :param X: input data
        :param frac_test: Fraction of input data to be used as test set
        :param frac_valid: Fraction of input data to be used as validation set
        :param CV: number of cross validation folds
        :param cv_splits_indices: List of tuples of the form (train, valid)
                                  where train and valid are both np arrays

        """
        if frac_test and frac_test >= 1.0:
            raise ValueError("Test set fraction set must be " +
                             "less than 1.0")

        if frac_valid and frac_valid >= 1.0:
            raise ValueError("Validation set fraction set must " +
                             "be less than 1.0")

        # sanity check on test and validation set percentage
        if frac_test and frac_valid and frac_test + frac_valid >= 1.0:
            raise ValueError("Sum of test and validation set fractions " +
                             "must be less than 1.0")

        # sanity check on CV
        if CV and CV <= 0:
            raise ValueError("The number of cross validations is " +
                             "less than or equal to zero")

        if cv_splits_indices:
            N = X.shape[0]
            full_index = np.arange(N)
            # check if the custon split is valid split.
            self._validate_custom_cv_splits(
                max_index=N, max_size=len(full_index),
                cv_splits_indices=cv_splits_indices)

    def _validate_custom_cv_splits(self, max_index, max_size,
                                   cv_splits_indices):
        """
        Validate the custom split indicies.

        :param max_index:
        :param max_size:
        :param cv_splits_indices:
        :return:
        """
        for train, valid in cv_splits_indices:
            for item in [train, valid]:
                if np.max(item) >= max_index:
                    raise ValueError(
                        "train index or valid index is out of bound")
                if np.min(item) < 0:
                    raise ValueError(
                        "train index or valid index is out of bound")
                if len(np.unique(item)) != item.shape[0]:
                    raise ValueError(
                        "train index or valid index has duplicates")

            if len(train) + len(valid) > max_size:
                raise ValueError(
                    "train index or valid index can not exceed size {0}"
                    .format(max_size))
            if np.intersect1d(train, valid).shape[0] != 0:
                raise ValueError("train index in cv split index and valid "
                                 "index have common values, cv-split indices "
                                 "should be disjoint")

    def _create_cv_splits(self, X, frac_test, frac_valid, CV,
                          cv_splits_indices, seed=123):
        """
        Create the cross validation split indicies
        :param X: input data
        :param seed: Integer value to set the random number state
        :param frac_test: Test set percent
        :param frac_valid: validation set percent
        :param CV: cross validation #
        :param cv_splits_indices: list of np arrays of train, valid indexes
        """
        if self._cv_split_type is None:
            raise ValueError("Cross validation type not found")

        N = X.shape[0]
        if cv_splits_indices:
            full_index = np.arange(N)
        else:
            np.random.seed(seed)
            full_index = np.random.permutation(N)

        if self._cv_split_type == _CVType.CustomCrossValitionSplit:
            # User specified custom cross validation splits
            self._CV_splits = cv_splits_indices
        elif self._cv_split_type == _CVType.KFoldCrossValitionSplit:
            # Generate CV splits for k-folds cross validation splits
            np.random.seed(seed)
            kf = model_selection.KFold(n_splits=CV)
            splits = []
            for train_index, valid_index in kf.split(full_index):
                splits.append(
                    (full_index[train_index], full_index[valid_index]))
            self._CV_splits = splits
        elif self._cv_split_type == _CVType.MonteCarloCrossValitionSplit:
            # Generate CV splits for k-folds cross validation splits with
            # user specified validation size
            np.random.seed(seed)
            splits = []
            full_size = len(full_index)
            for i in range(CV):
                full_index = full_index[np.random.permutation(
                    full_size)]
                splits.append((
                    full_index[:int(full_size * (1 - frac_valid))],
                    full_index[int(full_size * (1 - frac_valid)):]))
            self._CV_splits = splits
        elif self._cv_split_type == _CVType.TrainValitionPercSplit:
            # Generate train and validation set indices if
            # validation size is specified
            n_full = len(full_index)
            n_valid = int(frac_valid * N)
            n_train = n_full - n_valid
            np.random.seed(seed)
            shuffled_ind = np.random.permutation(full_index)
            valid_ind = shuffled_ind[n_train:]
            train_ind = shuffled_ind[:n_train]
            self._train_indices = train_ind
            self._valid_indices = valid_ind
        elif self._cv_split_type == _CVType.TrainTestValitionPercSplit:
            # Generate train, test and validation set indices if
            # validation size and test size is specified
            remaining_ind = full_index[:int(N * (1 - frac_test))]
            test_ind = full_index[int(N * (1 - frac_test)):]

            if not frac_valid:
                frac_valid = 0.1
            n_remaining = len(remaining_ind)
            n_valid = int(frac_valid * N)
            n_train = n_remaining - n_valid
            np.random.seed(seed)
            shuffled_ind = np.random.permutation(remaining_ind)
            valid_ind = shuffled_ind[n_train:]
            train_ind = shuffled_ind[:n_train]

            assert np.intersect1d(train_ind, test_ind).shape[0] == 0
            assert np.intersect1d(valid_ind, test_ind).shape[0] == 0

            self._train_indices = train_ind
            self._valid_indices = valid_ind
            self._test_indices = test_ind

    def apply_CV_splits(self, X, y, sample_weight):
        """
        Gets all the CV splits of the dataset, if cross validation is
        specified.
        :return:
        """
        if isinstance(X, pd.DataFrame):
            for train_ind, test_ind in self._CV_splits:
                yield (X.iloc[train_ind], y[train_ind],
                       None if sample_weight is None else sample_weight[
                           train_ind],
                       X.iloc[test_ind], y[test_ind],
                       None if sample_weight is None else sample_weight[
                           test_ind])
        elif isinstance(X, np.ndarray):
            for train_ind, test_ind in self._CV_splits:
                yield (X[train_ind], y[train_ind],
                       None if sample_weight is None else sample_weight[
                           train_ind],
                       X[test_ind], y[test_ind],
                       None if sample_weight is None else sample_weight[
                           test_ind])

    def get_train_validation_test_chunks(self, X, y, sample_weight):
        """
        Gets all the train, validation and test dataset, if percentage split is
        specified.
        :return:
        """
        X_train = None
        y_train = None
        sample_weight_train = None
        X_test = None
        y_test = None
        sample_weight_test = None
        X_valid = None
        y_valid = None
        sample_weight_valid = None
        if isinstance(X, pd.DataFrame):
            if self._train_indices is not None:
                X_train = X.iloc[self._train_indices]
            if self._test_indices is not None:
                X_test = X.iloc[self._test_indices]
            if self._valid_indices is not None:
                X_valid = X.iloc[self._valid_indices]
        elif isinstance(X, np.ndarray):
            if self._train_indices is not None:
                X_train = X[self._train_indices]
            if self._test_indices is not None:
                X_test = X[self._test_indices]
            if self._valid_indices is not None:
                X_valid = X[self._valid_indices]

        if self._train_indices is not None:
            y_train = y[self._train_indices]
            sample_weight_train = None if sample_weight is None \
                else sample_weight[self._train_indices]

        if self._test_indices is not None:
            y_test = y[self._test_indices]
            sample_weight_test = None if sample_weight is None \
                else sample_weight[self._test_indices]

        if self._valid_indices is not None:
            y_valid = y[self._valid_indices]
            sample_weight_valid = None if sample_weight is None \
                else sample_weight[self._valid_indices]

        return X_train, y_train, sample_weight_train, X_valid, y_valid, \
            sample_weight_valid, X_test, y_test, sample_weight_test


class _CVType:

    """
    Class for getting the different types of cross validation splits
    """
    TrainValitionPercSplit = "TrainValitionPercSplit"
    TrainTestValitionPercSplit = "TrainTestValitionPercSplit"
    CustomCrossValitionSplit = "CustomCorssValitionSplit"
    KFoldCrossValitionSplit = "KFoldCrossValitionSplit"
    MonteCarloCrossValitionSplit = "MonteCarloCrossValitionSplit"

    FULL_SET = {TrainValitionPercSplit,
                TrainTestValitionPercSplit,
                CustomCrossValitionSplit,
                KFoldCrossValitionSplit,
                MonteCarloCrossValitionSplit}


class FeaturizedCVSplit:
    """
    Class for keeping track of the featurized version of CV splits train and
    validation sets.
    """
    def __init__(self, X_train_transformed, y_train, sample_wt_train,
                 X_test_transformed, y_test, sample_wt_test,
                 data_transformer=None,
                 lag_transformer=None):
        self._X_train_transformed = X_train_transformed
        self._y_train = y_train
        self._sample_wt_train = sample_wt_train
        self._X_test_transformed = X_test_transformed
        self._y_test = y_test
        self._sample_wt_test = sample_wt_test
        self._data_transformer = data_transformer
        self._lag_transformer = lag_transformer

    def __str__(self):
        """
        Return the string version of the members in this class
        """
        some_str = "_X_train_transformed: " + str(self._X_train_transformed.shape) + "\n"
        some_str += "y_train: " + str(self._y_train.shape) + "\n"
        if self._sample_wt_train is not None:
            some_str += "sample_wt_train: " + str(self._sample_wt_train.shape) + "\n"
        if self._X_test_transformed is not None:
            some_str += "X_test_transformed: " + str(self._X_test_transformed.shape) + "\n"
        if self._y_test is not None:
            some_str += "y_test: " + str(self._y_test.shape) + "\n"
        if self._sample_wt_test is not None:
            some_str += "sample_wt_test: " + str(self._sample_wt_test.shape) + "\n"
        return some_str


class FeaturizedTrainValidTestSplit(FeaturizedCVSplit):
    """
    Class for keeping track of the featurized version of train, test and
    validation sets.
    """
    def __init__(self, X_train_transformed, y_train, sample_wt_train,
                 X_valid_transformed, y_valid, sample_wt_valid,
                 X_test_transformed, y_test, sample_wt_test,
                 data_transformer=None,
                 lag_transformer=None):
        super().__init__(X_train_transformed, y_train, sample_wt_train,
                         X_test_transformed, y_test, sample_wt_test,
                         data_transformer, lag_transformer)

        self._X_valid_transformed = X_valid_transformed
        self._y_valid = y_valid
        self._sample_wt_valid = sample_wt_valid

    def __str__(self):
        """
        Return the string version of the members in this class
        """
        some_str = "_X_train_transformed: " + str(self._X_train_transformed.shape) + "\n"
        some_str += "y_train: " + str(self._y_train.shape) + "\n"
        if self._sample_wt_train is not None:
            some_str += "sample_wt_train: " + str(self._sample_wt_train.shape) + "\n"
        if self._X_test_transformed is not None:
            some_str += "X_test_transformed: " + \
                str(self._X_test_transformed.shape) + "\n"
        if self._y_test is not None:
            some_str += "y_test: " + str(self._y_test.shape) + "\n"
        if self._sample_wt_test is not None:
            some_str += "sample_wt_test: " + str(self._sample_wt_test.shape) + "\n"
        if self._X_valid_transformed is not None:
            some_str += "X_valid_transformed: " + str(self._X_valid_transformed.shape) + "\n"
        if self._y_valid is not None:
            some_str += "y_valid: " + str(self._y_valid.shape) + "\n"
        if self._sample_wt_valid is not None:
            some_str += "sample_wt_valid: " + str(self._sample_wt_valid.shape) + "\n"

        return some_str
