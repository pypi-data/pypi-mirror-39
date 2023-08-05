# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for processing datasets for training/validation."""
import copy
import math
import sys

import numpy as np
import scipy
import sklearn
from sklearn import model_selection

from automl.client.core.common import constants, problem_info, utilities
from automl.client.core.common.utilities import sparse_std
from automl.client.core.common._cv_splits import _CVSplits, _CVType


class SubsampleCacheStrategy:
    """
    Different cache strategy for subsampling caching on training set.
    Classic: Sample for the specified sample size, cache the result.
    ClassicNoCache: Same as Classic, but the result is not cached.
    Preshuffle: Shuffle the train set indices on the first sampling call.
        Return the first specified percentage of data. The subsequent calls
        also return the first specified percentage.

    If we want to sample the dataset a few times with consistent
        result, use Classic.
    If we want to sample the dataset many times with consistent
        result, use Preshuffle.
    If we want to sample the dataset once, or resample everytime,
        use ClassicNoCache.
    """
    Classic = "Classic"
    ClassicNoCache = "ClassicNoCache"
    Preshuffle = "Preshuffle"


class ClientDatasets(object):
    """
    The object to stote the experiment input data and training charateristics
    """

    # TODO: it would be nice to codify all these.
    TRAIN_CV_SPLITS = 'train CV splits'
    FEATURIZED_TRAIN_CV_SPLITS = 'featurized train CV splits'
    FEATURIZED_TRAIN = 'featurized train'
    FEATURIZED_TEST = 'featurized test'
    FEATURIZED_VALID = 'featurized valid'
    TRAIN = 'train indices'
    TEST = 'test indices'
    VALID = 'valid indices'

    def __init__(self, meta_data=None,
                 subsample_cache_strategy=SubsampleCacheStrategy.Classic):
        """
        Various methods for processing datasets for training/validation.
        :param meta_data: metedata to be directly set on the dataset.
        :param subsample_cache_strategy: SubsampleCacheStrategy value for
            subsample cache strategy.
        """
        self._dataset = meta_data or {}
        self.binary_fields = [
            'X', 'y',
            ClientDatasets.TRAIN, ClientDatasets.FEATURIZED_TRAIN,
            ClientDatasets.TEST, ClientDatasets.FEATURIZED_TEST,
            ClientDatasets.VALID, ClientDatasets.FEATURIZED_VALID,
            ClientDatasets.TRAIN_CV_SPLITS,
            ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]
        self.meta_fields = [
            'dataset_id', 'num_samples', 'num_features', 'num_categorical',
            'num_classes', 'num_missing', 'y_mean', 'y_std', 'y_min', 'y_max',
            'X_mean', 'X_std', 'task', 'openml_id', 'name', 'is_sparse',
            'class_labels', 'y_transformer']
        self._subsample_cache_strategy = subsample_cache_strategy
        self._subsample_cache = {}
        self._shuffled_train_indices = None

    def get_y_range(self):
        """
        Gets the range of y values.
        :return: The y_min and y_max value.
        """
        y_min, y_max = None, None
        if 'y_min' in self._dataset:
            y_min = self._dataset['y_min']
        if 'y_max' in self._dataset:
            y_max = self._dataset['y_max']
        return y_min, y_max

    def get_y_std(self):
        return self.get_meta('y_std')

    def get_full_set(self):
        """
        returns the full dataset sample data and label
        :return: return the full dataset
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        return X, y, sample_weight

    def get_train_set(self):
        """
        returns the training part of the dataset
        :return:
        """
        X_train = None
        y_train = None
        sample_weight_train = None
        if ClientDatasets.TRAIN in self._dataset:
            X, y = self._dataset['X'], self._dataset['y']
            sample_weight = self._dataset.get('sample_weight')
            X_train, y_train = X[self._dataset[ClientDatasets.TRAIN]], y[
                self._dataset[ClientDatasets.TRAIN]]
            sample_weight_train = None \
                if sample_weight is None \
                else sample_weight[self._dataset[ClientDatasets.TRAIN]]
        elif ClientDatasets.FEATURIZED_TRAIN in self._dataset:
            X_train = self._dataset[ClientDatasets.FEATURIZED_TRAIN]['X']
            y_train = self._dataset[ClientDatasets.FEATURIZED_TRAIN]['y']
            sample_weight_train = \
                self._dataset[ClientDatasets.FEATURIZED_TRAIN]['sample_weight']

        return X_train, y_train, sample_weight_train

    def get_valid_set(self):
        """
        returns the validation part of the dataset
        :return:
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        X_valid = None
        y_valid = None
        sample_weight_valid = None
        if 'X_valid' in self._dataset:
            assert 'y_valid' in self._dataset
            X_valid, y_valid, sample_weight_valid = (
                self._dataset['X_valid'],
                self._dataset['y_valid'],
                None)
            if sample_weight is not None:
                sample_weight_valid = self._dataset['sample_weight_valid']
        elif ClientDatasets.VALID in self._dataset:
            X_valid, y_valid = (
                X[self._dataset[ClientDatasets.VALID]],
                y[self._dataset[ClientDatasets.VALID]])
            sample_weight_valid = (None
                                   if sample_weight is None
                                   else sample_weight[
                                       self._dataset[ClientDatasets.VALID]])
        elif ClientDatasets.FEATURIZED_VALID in self._dataset:
            X_valid = self._dataset[ClientDatasets.FEATURIZED_VALID]['X']
            y_valid = self._dataset[ClientDatasets.FEATURIZED_VALID]['y']
            sample_weight_valid = \
                self._dataset[ClientDatasets.FEATURIZED_VALID]['sample_weight']

        return X_valid, y_valid, sample_weight_valid

    def get_y_transformer(self):
        """
        return the y_transformer.
        """
        return self._dataset.get('y_transformer')

    def get_test_set(self):
        """
        Get the test set from the full dataset
        :return: Test features, test labels, and weights of test samples
        :rtype: tuple(np.ndarray, np.ndarray, np.ndarray)
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        X_test = None
        y_test = None
        sample_weight_test = None
        if 'X_test' in self._dataset:
            assert 'y_test' in self._dataset.keys()
            X_test, y_test = self._dataset['X_test'], self._dataset['y_test']
            sample_weight_test = self._dataset['sample_weight_test']
        elif ClientDatasets.TEST in self._dataset:
            X_test, y_test = X[self._dataset[ClientDatasets.TEST]
                               ], y[self._dataset[ClientDatasets.TEST]]
            sample_weight_test = (sample_weight and
                                  sample_weight[self._dataset[
                                      ClientDatasets.TEST]])
        elif ClientDatasets.FEATURIZED_TEST in self._dataset:
            X_test = self._dataset[ClientDatasets.FEATURIZED_TEST]['X']
            y_test = self._dataset[ClientDatasets.FEATURIZED_TEST]['y']
            sample_weight_test = \
                self._dataset[ClientDatasets.FEATURIZED_TEST]['sample_weight']

        return X_test, y_test, sample_weight_test

    def has_test_set(self):
        """
        returns if the given dataset has test set available
        :return:
        """
        return 'X_test' in self._dataset and \
            self._dataset['X_test'].any() or \
            ClientDatasets.TEST in self._dataset or \
            ClientDatasets.FEATURIZED_TEST in self._dataset

    def has_training_set(self):
        """
        returns if the given dataset has training set available
        :return:
        """
        return ClientDatasets.TRAIN in self._dataset or \
            ClientDatasets.FEATURIZED_TRAIN in self._dataset

    def get_CV_splits(self):
        """
        gets the CV splits of the dataset, if cross validation is specified.
        :return:
        """
        if self._dataset.get(ClientDatasets.TRAIN_CV_SPLITS) is not None:
            sample_wt = self._dataset.get('sample_weight')
            for train_ind, test_ind in self._dataset[
                    ClientDatasets.TRAIN_CV_SPLITS]:
                yield (self._dataset['X'][train_ind],
                       self._dataset['y'][train_ind],
                       None if sample_wt is None else sample_wt[train_ind],
                       self._dataset['X'][test_ind],
                       self._dataset['y'][test_ind],
                       None if sample_wt is None else sample_wt[test_ind])

        elif self._dataset.get(ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS) is not None:
            for featurized_cv_split in self._dataset[
                    ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]:
                yield (
                    featurized_cv_split._X_train_transformed,
                    featurized_cv_split._y_train,
                    featurized_cv_split._sample_wt_train,
                    featurized_cv_split._X_test_transformed,
                    featurized_cv_split._y_test,
                    featurized_cv_split._sample_wt_test)
        else:
            raise ValueError('CV splits not found in dataset.')

    def get_num_classes(self):
        """
        gets the number of classes in the dataset.
        :return:  number of classes
        """
        return self.get_meta('num_classes')

    def get_class_labels(self):
        """Gets the class labels for a classification task"""
        return self.get_meta('class_labels')

    def get_task(self):
        """
        return the current task type
        :return:  task type such as regression or classification.
        """
        return self.get_meta('task')

    def get_meta(self, attr):
        """
        returns the value of the dataset attribute such as task, y_max
        :param attr:  the attribute to get
        :return: returns the value of the passed attribute
        """
        return self._dataset.get(attr, None)

    def get_is_sparse(self):
        """
        returns whether the dataset is sparse format.
        """
        is_sparse = self._dataset.get('is_sparse', None)
        if is_sparse is None:
            is_sparse = scipy.sparse.issparse(self._dataset['X'])
            self._dataset['is_sparse'] = is_sparse
        return is_sparse

    def add_data(self, attr, val):
        """
        sets the value of a datasetattribute
        :param attr: the attribute to set the value
        :param val: the value of the attribute
        :return: none
        """
        self._dataset[attr] = val

    def get_problem_info(self):
        """
        returns the _ProblemInfo of the dataset
        :return:
        """
        return problem_info.ProblemInfo(
            dataset_samples=self.get_meta('num_samples'),
            dataset_classes=self.get_num_classes(),
            dataset_features=self.get_meta('num_features'),
            dataset_num_categorical=self.get_meta('num_categorical'),
            dataset_y_std=self.get_meta('y_std'),
            is_sparse=self.get_meta('is_sparse'),
            task=self.get_meta('task'),
            metric=None)

    def _init_dataset(self, name, task, X, y, sample_weight=None,
                      categorical=None, openml_id=None, num_classes=None,
                      y_min=None, y_max=None, y_transformer=None,
                      init_all_stats=True):
        """
        Initialize the data set with the input data, metadata and labels
        :param name:
        :param X: train data
        :param y: label for train data
        :param task: the task type of training(regression/classification)
        :param sample_weight: size of the sample
        :param categorical: is it categorical?
        :param openml_id:
        :param num_classes: number of classes in the experiment.
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param init_all_stats:
        :param y_transformer: If is not None, then do inverse transform.
        :return:
        """
        self._dataset = {}
        if openml_id is not None:
            self._dataset['openml_id'] = openml_id
        else:
            self._dataset['openml_id'] = 'NA'
        self._dataset['dataset_id'] = name
        self._dataset['name'] = name
        self._dataset['num_samples'] = int(X.shape[0])
        self._dataset['num_features'] = int(X.shape[1])
        self._dataset['num_missing'] = 0 if scipy.sparse.issparse(
            X) else int(np.sum(np.isnan(X)))
        self._dataset['y_std'] = float(y.std())
        if init_all_stats:
            self._dataset['y_mean'] = float(y.mean())
            self._dataset['X_mean'] = float(X.mean())
            self._dataset['X_std'] = float(
                X.std()) if not scipy.sparse.issparse(X) \
                else utilities.sparse_std(X)
            self._dataset['is_sparse'] = scipy.sparse.issparse(X)
        else:
            self._dataset['y_mean'] = None
            self._dataset['X_mean'] = None
            self._dataset['X_std'] = None
            self._dataset['is_sparse'] = None

        self._dataset['y_min'] = y_min if y_min else float(y.min())
        self._dataset['y_max'] = y_max if y_max else float(y.max())

        if categorical is None:
            # assume 0, but we really don't know in this case.
            self._dataset['num_categorical'] = 0
        else:
            self._dataset['num_categorical'] = int(np.sum(categorical))

        self._dataset['task'] = task
        if task == constants.Tasks.CLASSIFICATION:
            if num_classes is None:
                self._dataset['num_classes'] = len(np.unique(y))
            else:
                self._dataset['num_classes'] = num_classes
            self._dataset['class_labels'] = np.unique(y)
        elif task == constants.Tasks.REGRESSION:
            self._dataset['num_classes'] = None

        for k in self._dataset.keys():
            assert k in self.meta_fields, "%s is not in meta_fields" % k

        self._dataset['X'] = X
        self._dataset['y'] = y
        self._dataset['y_transformer'] = y_transformer
        self._dataset['sample_weight'] = sample_weight
        self._dataset['sample_weight_valid'] = None
        self._dataset['sample_weight_test'] = None

    def parse_simple_train_validate(self,
                                    name,
                                    task,
                                    X, y,
                                    X_valid, y_valid,
                                    sample_weight=None,
                                    sample_weight_valid=None,
                                    num_classes=None,
                                    y_min=None,
                                    y_max=None,
                                    y_transformer=None,
                                    init_all_stats=True):
        """
        creates a ClientDataset processing the input data

        :param name:
        :param task: task type
        :param X: train data
        :param y: label
        :param sample_weight:
        :param X_valid: validation data
        :param y_valid: validation label
        :param sample_weight_valid:
        :param num_classes: number of classes in the experiment
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param y_transformer: If is not None, then do inverse transform.
        :return: a client dataset woth all metadata set.
        """
        if num_classes is None:
            num_classes = np.unique(np.concatenate(
                (np.unique(y), np.unique(y_valid)), axis=0)).shape[0]
        self._init_dataset(
            name, task, X, y, sample_weight=sample_weight,
            num_classes=num_classes, y_min=y_min, y_max=y_max,
            y_transformer=y_transformer, init_all_stats=init_all_stats)

        self._dataset['X_valid'] = X_valid
        self._dataset['y_valid'] = y_valid
        self._dataset["sample_weight"] = sample_weight
        self._dataset['sample_weight_valid'] = sample_weight_valid
        self._dataset[ClientDatasets.TRAIN] = np.arange(X.shape[0])

        if self._dataset['task'] == constants.Tasks.REGRESSION:
            self._dataset['bin_info'] = self.make_bin_info(X_valid.shape[0], y)

    def parse_data(self, name, task, X, y, sample_weight=None,
                   categorical=None, cv_splits=None,
                   openml_id=None, num_classes=None,
                   y_min=None, y_max=None, y_transformer=None,
                   init_all_stats=True):
        """
        :param name:
        :param task: task type
        :param X: input data
        :param y: label
        :param sample_weight:
        :param cv_splits: Carries CV splits information
        :type cv_splits: automl.client.core.common._cv_splits
        :param categorical: is it categorical?
        :param openml_id:
        :param num_classes: number of classes in the experiment
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param y_transformer: If is not None, then do inverse transform.
        :param init_all_stats: Flag to compute stats
        :return: a client dataset woth all metadata set.
        """

        # Initialize all the stats
        self._init_dataset(name, task, X, y,
                           sample_weight=sample_weight,
                           categorical=categorical, openml_id=openml_id,
                           num_classes=num_classes,
                           y_min=y_min, y_max=y_max,
                           y_transformer=y_transformer,
                           init_all_stats=init_all_stats)

        if cv_splits is not None:
            # Based on the type of CV split populate all the bin info for
            # regression tasks
            cv_split_type = cv_splits.get_cv_split_type()
            if task == constants.Tasks.REGRESSION:
                if cv_split_type == _CVType.CustomCrossValitionSplit:
                    self._dataset['bin_info'] = self.make_bin_info(
                        np.min([len(split[1]) for split in
                                cv_splits.get_cv_split_indices()]),
                        self._dataset['y'])
                elif cv_split_type == _CVType.KFoldCrossValitionSplit:
                    self._dataset['bin_info'] = self.make_bin_info(
                        int(self._dataset['num_samples'] / cv_splits.get_num_k_folds()),
                        self._dataset['y'])
                elif cv_split_type == _CVType.MonteCarloCrossValitionSplit:
                    self._dataset['bin_info'] = self.make_bin_info(
                        int(self._dataset['num_samples'] * cv_splits.get_fraction_validation_size()),
                        self._dataset['y'])
                else:
                    if 'bin_info' not in self._dataset:
                        self._dataset['bin_info'] = self.make_bin_info(
                            int(self._dataset['num_samples'] * cv_splits.get_fraction_validation_size()),
                            self._dataset['y'])

            self._dataset[ClientDatasets.TRAIN_CV_SPLITS] = None
            self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = None
            # Populate the CV splits indicies
            if cv_split_type != _CVType.TrainTestValitionPercSplit and \
               cv_split_type != _CVType.TrainValitionPercSplit:

                if cv_splits.get_featurized_cv_split_data() is None:
                    self._dataset[ClientDatasets.TRAIN_CV_SPLITS] = cv_splits.get_cv_split_indices()
                else:
                    self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = \
                        cv_splits.get_featurized_cv_split_data()
            else:
                if cv_splits._featurized_train_test_valid_chunks is None:
                    train_indices, test_indices, valid_indices = cv_splits.get_train_test_valid_indices()
                    self._dataset[ClientDatasets.TRAIN] = train_indices
                    self._dataset[ClientDatasets.VALID] = valid_indices
                    if cv_splits._cv_split_type == _CVType.TrainTestValitionPercSplit:
                        self._dataset[ClientDatasets.TEST] = test_indices
                else:
                    featurized_train_data, featurized_test_data, featurized_valid_data = \
                        cv_splits.get_featurized_train_test_valid_data()
                    self._dataset[ClientDatasets.FEATURIZED_TRAIN] = featurized_train_data
                    self._dataset[ClientDatasets.FEATURIZED_VALID] = featurized_valid_data
                    if cv_splits._cv_split_type == _CVType.TrainTestValitionPercSplit:
                        self._dataset[ClientDatasets.FEATURIZED_TEST] = featurized_test_data

    def make_bin_info(self, n_valid, y):
        """
        creates dictionary y binned with points in y.
        :param n_valid: number of points in validation set
        :param y: labels to be binned
        :return:
        """
        default_num_bins, min_points_per_bin, percentile,\
            extra_outlier_bins = 100, 10, 1, 2
        if int(n_valid / default_num_bins) >= min_points_per_bin:
            num_bins_major_perc = default_num_bins
        else:
            num_bins_major_perc = int(n_valid / min_points_per_bin) -\
                extra_outlier_bins
        num_bins = num_bins_major_perc + extra_outlier_bins
        if num_bins <= 0:
            raise ValueError('y_valid only has {} items which is smaller than '
                             'the minimum allowable value {}. Please try '
                             'again with a larger validation set.'
                             .format(n_valid, min_points_per_bin))
        first_bin_end, last_bin_start = np.percentile(
            y, [percentile, 100 - percentile], interpolation='nearest')
        bin_dict = {'number_of_bins': num_bins, 'bin_starts': np.zeros(
            num_bins), 'bin_ends': np.zeros(num_bins)}
        bin_dict['bin_starts'][0], bin_dict['bin_ends'][0] = y.min(), first_bin_end
        bin_dict['bin_starts'][-1], bin_dict['bin_ends'][-1] = last_bin_start, y.max()

        bin_width_major_perc = (last_bin_start - first_bin_end) / num_bins_major_perc

        if bin_width_major_perc >= 1:
            # For numbers greater than 1, preserve 2 decimal places when rounding
            bin_dict['bin_starts'][1:num_bins - 1] = \
                [np.around(first_bin_end + x * bin_width_major_perc, decimals=2)
                 for x in range(num_bins_major_perc)]
        else:
            # Attempt to round so we preserve 2 sigfigs of the width
            num_decimal_places = -1 * int(np.log10(bin_width_major_perc)) + 2
            bin_dict['bin_starts'][1:num_bins - 1] = \
                [np.around(first_bin_end + x * bin_width_major_perc, decimals=num_decimal_places)
                 for x in range(num_bins_major_perc)]
        bin_dict['bin_ends'][1:num_bins -
                             1] = bin_dict['bin_starts'][2:num_bins]
        return bin_dict

    def get_bin_info(self):
        return self.get_meta('bin_info')

    def get_subsampled_dataset(self, subsample_percent,
                               force_resample=False, random_state=None):
        """

        :param original_dataset:
        :param subsample_percent:
        :param random_state: int, RandomState instance or None, optional
            (default=None) If int, random_state is the seed used by the
            random number generator; If RandomState instance, random_state
            is the random number generator; If None, the random number
            generator is the RandomState instance used by `np.random`.
        :return: Another ClientDatasets object that is a subsample.
        """
        assert subsample_percent > 0 and subsample_percent < 100

        if not force_resample and subsample_percent in self._subsample_cache:
            return self._subsample_cache[subsample_percent]

        subsample_frac = float(subsample_percent) / 100.0

        # shallow copy the dataset
        ret = ClientDatasets(
            subsample_cache_strategy=self._subsample_cache_strategy)
        ret._dataset = copy.copy(self._dataset)

        if ClientDatasets.TRAIN in self._dataset:
            train_y = None
            if self.get_meta('task') == constants.Tasks.CLASSIFICATION:
                train_y = self._dataset['y'][self._dataset[
                    ClientDatasets.TRAIN]]

            if self._subsample_cache_strategy == \
                    SubsampleCacheStrategy.Preshuffle:
                self._shuffled_train_indices = utilities.stratified_shuffle(
                    self._dataset[ClientDatasets.TRAIN], train_y, random_state)
                subsample_count = math.ceil(len(self._shuffled_train_indices) *
                                            subsample_frac)
                ret._dataset[ClientDatasets.TRAIN] = \
                    self._shuffled_train_indices[:subsample_count]
            else:
                new_train_indices, _ = model_selection.train_test_split(
                    self._dataset[ClientDatasets.TRAIN],
                    train_size=subsample_frac,
                    stratify=train_y,
                    random_state=random_state)
                ret._dataset[ClientDatasets.TRAIN] = new_train_indices

        else:
            # for CV
            ret._dataset[ClientDatasets.TRAIN_CV_SPLITS] = copy.copy(
                self._dataset[ClientDatasets.TRAIN_CV_SPLITS])
            for i, item in enumerate(ret._dataset[
                    ClientDatasets.TRAIN_CV_SPLITS]):
                train, test = item
                original_n = len(train)
                subsample_n = int(original_n * subsample_frac)
                sub_train = train[:subsample_n]
                ret._dataset[
                    ClientDatasets.TRAIN_CV_SPLITS][i] = (sub_train, test)

                assert subsample_n == len(
                    ret._dataset[ClientDatasets.TRAIN_CV_SPLITS][i][0])
                assert original_n == len(
                    self._dataset[ClientDatasets.TRAIN_CV_SPLITS][i][0])

        if self._subsample_cache_strategy != \
                SubsampleCacheStrategy.ClassicNoCache:
            self._subsample_cache[subsample_percent] = ret

        return ret

    @staticmethod
    def _check_data(X, y, categorical=None, missing_data=False):
        """

        :param X:
        :param y:
        :param categorical:
        :param missing_data:
        :return:
        """
        if not missing_data:
            assert (isinstance(X, np.ndarray) and not np.any(
                np.isnan(X))) or scipy.sparse.issparse(X)

        if categorical is not None:
            assert X.shape[1] == len(
                categorical), ("there should be one categorical indicator "
                               "for each feature")

        assert not np.any(np.isnan(y)), "can't have any missing values in y"
        assert X.shape[0] == y.shape[0], "X and y should have the same shape"
        assert len(y.shape) == 2, "y should be a vector Nx1"
        assert y.shape[1] == 1, "y should be a vector Nx1"

    @staticmethod
    def _encode_data(X, y, categorical):
        """

        :param X:
        :param y:
        :param categorical:
        :return:
        """
        if np.any(categorical):
            enc = sklearn.preprocessing.OneHotEncoder(
                categorical_features=categorical)
            X = enc.fit_transform(X).todense()
        return X, y

    @staticmethod
    def get_dataset(
            name, X, y, task, sample_weight=None, missing_data=False,
            categorical=None, seed=123, perc_test=0.1, perc_valid=0.1, CV=10,
            cv_splits_indices=None, openml_id=None, y_min=None, y_max=None,
            subsample_cache_strategy=SubsampleCacheStrategy.Classic,
            y_transformer=None):
        """

        :param name:
        :param X:
        :param y:
        :param sample_weight:
        :param missing_data:
        :param categorical:
        :param task:
        :param seed:
        :param perc_test:
        :param perc_valid:
        :param CV:
        :param cv_splits_indices:
        :param openml_id:
        :param y_min:
        :param y_max:
        :param y_transformer:
        :return:
        """
        ClientDatasets._check_data(X, y, categorical, missing_data)
        if categorical is not None:
            X, y = ClientDatasets._encode_data(X, y, categorical)

        ret = ClientDatasets(
            subsample_cache_strategy=subsample_cache_strategy)
        cv_splits = _CVSplits(X, y, seed=seed, frac_test=perc_test,
                              frac_valid=perc_valid,
                              CV=CV)
        ret.parse_data(
            name=name, task=task, X=X, y=y, sample_weight=sample_weight,
            categorical=categorical, cv_splits=cv_splits, openml_id=openml_id,
            y_min=y_min, y_max=y_max, y_transformer=y_transformer)
        return ret


if __name__ == '__main__':
    pass
