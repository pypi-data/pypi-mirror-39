# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Runner class used for each iteration of an AutoML execution."""
import copy
import datetime

import numpy as np
import pickle
import scipy
import sklearn
import sklearn.metrics  # noqa F401
import sklearn.preprocessing  # noqa F401
from sklearn.pipeline import Pipeline, make_pipeline  # noqa F401

from automl.client.core.common import metrics as mt
from automl.client.core.common.constants import (Metric,
                                                 Sample_Weights_Unsupported,
                                                 Tasks, TrainingType)
from automl.client.core.common.resource_limits import (default_resource_limits,
                                                       safe_enforce_limits)

from automl.client.core.common.metrics import (
    compute_metrics_classification, compute_metrics_regression,
    get_default_metrics)


class ClientRunner(object):
    """
    Original/Legacy Runner which encapsulates the fit() method for various
    AutoML models.
    """

    def __init__(self,
                 datasets,
                 metrics=None,
                 runtime_constraints=None,
                 task_type=None):
        """

        :param datasets:
        :param metrics:
        :param runtime_constraints:
        :param task_type:
        """

        if metrics is None:
            metrics = mt.get_default_metrics(task=task_type)

        if runtime_constraints is None:
            runtime_constraints = default_resource_limits
        self.runtime_constraints = runtime_constraints

        self.metrics = metrics
        self.datasets = datasets
        self.task_type = task_type

    def time_fit(self, m, X, y, sample_weight=None):
        """

        :param m:
        :param X:
        :param y:
        :return:
        """
        t = datetime.datetime.utcnow()  # time.process_time()
        kwargs = {}
        if sample_weight is not None:
            # get model's name in steps array
            clf = m.steps[-1][0]
            if clf not in Sample_Weights_Unsupported:
                # pipeline expects kwargs to be formatted as stepname__arg.
                # The arg is then passed to fit of stepname
                kwargs = {clf + "__sample_weight": sample_weight}
        fitted_model = m.fit(X, y.ravel(), **kwargs)
        elapsed_time = datetime.datetime.utcnow() - t
        return elapsed_time.seconds, fitted_model

    def time_fit_ensemble(self, m, training_type, dataset, sample_weight=None):
        """

        :param m:
        :param X:
        :param y:
        :return:
        """
        t = datetime.datetime.utcnow()  # time.process_time()
        kwargs = {}
        if sample_weight is not None:
            # get model's name in steps array
            clf = m.steps[-1][0]
            if clf not in Sample_Weights_Unsupported:
                # pipeline expects kwargs to be formatted as stepname__arg.
                # The arg is then passed to fit of stepname
                kwargs = {clf + "__sample_weight": sample_weight}
        fitted_ensemble_model, cv_ensembles = m._final_estimator.fit_ensemble(
            training_type, dataset, **kwargs)
        elapsed_time = datetime.datetime.utcnow() - t
        return elapsed_time.seconds, fitted_ensemble_model, cv_ensembles

    def _compute_metric(self, pipeline, X, y,
                        num_classes=None, class_labels=None,
                        y_min=None, y_max=None, y_std=None,
                        sample_weight=None,
                        bin_info=None,
                        y_transformer=None):
        """

        :param pipeline:
        :param X:
        :param y:
        :param num_classes:
        :param y_min:
        :param y_max:
        :param y_std:
        :param bin_info:
        :param class_labels:
        :param y_transformer:
        :return:
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("Mismatch validation data shape X={}, y={}"
                             .format(X.shape, y.shape))
        if self.task_type == Tasks.CLASSIFICATION:
            if hasattr(pipeline, 'predict_proba'):
                y_pred_probs = pipeline.predict_proba(X)
                return compute_metrics_classification(
                    y_pred_probs=y_pred_probs, y_test=y,
                    metrics=self.metrics, num_classes=num_classes,
                    sample_weight=sample_weight, class_labels=class_labels,
                    y_transformer=y_transformer)
            else:
                y_predicted = pipeline.predict(X)
                return self.compute_metrics_classification_legacy(
                    y_pred=y_predicted, y_test=y, metrics=self.metrics,
                    num_classes=num_classes,
                    sample_weight=sample_weight)
        elif self.task_type == Tasks.REGRESSION:
            y_predicted = pipeline.predict(X)
            return compute_metrics_regression(
                y_pred=y_predicted, y_test=y, metrics=self.metrics,
                y_min=y_min, y_max=y_max, y_std=y_std,
                sample_weight=sample_weight,
                bin_info=bin_info)
        else:
            raise NotImplementedError

    def _get_task_params(self, dataset):
        num_classes = None
        class_labels = None
        y_min = None
        y_max = None
        y_std = None
        bin_info = None

        if self.task_type == Tasks.CLASSIFICATION:
            num_classes = dataset.get_num_classes()
            class_labels = dataset.get_class_labels()
        elif self.task_type == Tasks.REGRESSION:
            y_min, y_max = dataset.get_y_range()
            y_std = dataset.get_y_std()
            bin_info = dataset.get_bin_info()
        else:
            raise NotImplementedError
        return num_classes, class_labels, y_min, y_max, y_std, bin_info

    def _run_train_valid(self, dataset, pipeline_spec):
        """

        :param dataset:
        :param pipeline_spec:
        :return:
        """
        num_classes, class_labels, y_min, y_max, \
            y_std, bin_info = self._get_task_params(dataset=dataset)
        m = pipeline_spec
        X_train, y_train, sample_weight_train = dataset.get_train_set()
        X_valid, y_valid, sample_weight_valid = dataset.get_valid_set()
        y_transformer = dataset.get_y_transformer()
        fit_time, fit_model = self.time_fit(
            m, X_train, y_train, sample_weight=sample_weight_train)
        score_valid = self._compute_metric(
            pipeline=m, X=X_valid, y=y_valid, num_classes=num_classes,
            y_min=y_min, y_max=y_max, y_std=y_std,
            sample_weight=sample_weight_valid,
            bin_info=bin_info,
            class_labels=class_labels,
            y_transformer=y_transformer)
        return score_valid, fit_time, m, fit_model

    def _run_train_full(self, dataset, pipeline_spec):
        """=

        :param dataset:
        :param pipeline_spec:
        :return:
        """
        num_classes, class_labels, y_min, y_max, \
            y_std, bin_info = self._get_task_params(dataset=dataset)
        m = pipeline_spec
        y_transformer = dataset.get_y_transformer()
        if dataset.has_training_set():
            X_train, y_train, sample_weight_train = dataset.get_train_set()
            X_valid, y_valid, sample_weight_valid = dataset.get_valid_set()
            X_full = scipy.sparse.vstack((X_train, X_valid)) if \
                scipy.sparse.issparse(X_train) \
                else np.concatenate((X_train, X_valid))
            y_full = np.concatenate((y_train, y_valid))
            if sample_weight_valid is not None:
                sample_weight_full = np.concatenate(
                    (sample_weight_train, sample_weight_valid))
            else:
                sample_weight_full = None
        else:
            X_full, y_full, sample_weight_full = dataset.get_full_set()

        fit_time, fit_model = self.time_fit(
            m, X_full, y_full, sample_weight=sample_weight_full)
        score_full = self._compute_metric(
            pipeline=m, X=X_full, y=y_full, num_classes=num_classes,
            y_min=y_min, y_max=y_max, y_std=y_std,
            sample_weight=sample_weight_full,
            bin_info=bin_info,
            class_labels=class_labels,
            y_transformer=y_transformer)
        return score_full, fit_time, m, fit_model

    def _run_cv(self, dataset, pipeline_spec):
        """

        :param dataset:
        :param pipeline_spec:
        :return:
        """
        X, y, sample_weight = dataset.get_full_set()
        y_transformer = dataset.get_y_transformer()
        num_classes, class_labels, y_min, y_max, \
            y_std, bin_info = self._get_task_params(dataset=dataset)
        scores = []
        fit_times = []
        models = []
        fit_models = []
        for X_train, y_train, sample_wt_train, X_test, y_test, sample_wt_test \
                in dataset.get_CV_splits():
            # create a clone of the pipeline so that there is no iterference
            # between the folds
            serialized = pickle.dumps(pipeline_spec)
            m = pickle.loads(serialized)

            fit_time, fit_model = self.time_fit(
                m, X_train, y_train, sample_wt_train)
            score = self._compute_metric(
                pipeline=m, X=X_test, y=y_test, num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                sample_weight=sample_wt_test,
                bin_info=bin_info,
                class_labels=class_labels,
                y_transformer=y_transformer)
            scores.append(score)
            fit_times.append(fit_time)
            models.append(m)
            fit_models.append(fit_model)
        return scores, fit_times, models, fit_models

    def _run_cv_mean(self, dataset, pipeline_spec,
                     cv_results=None, y_transformer=None):
        """

        :param dataset:
        :param pipeline_spec:
        :param cv_results:
        :param y_transformer:
        :return:
        """
        if cv_results is None:
            scores, fit_times, models, fit_models = self._run_cv(
                dataset, pipeline_spec)
        else:
            scores, fit_times, models, fit_models = cv_results

        mean_time = float(np.mean(fit_times))
        mean_scores = self._get_mean_cv_scores(scores)

        return mean_scores, mean_time, models, fit_models

    def _get_mean_cv_scores(self, scores):
        mean_scores = {}
        for k in self.metrics:
            split_results = []
            if k in scores[0].keys():
                for score in scores:
                    split_results.append(score[k])

                if np.isscalar(split_results[0]):
                    mean_scores[k] = float(np.mean(split_results))
                elif k in [Metric.AccuracyTable,
                           Metric.ConfusionMatrix,
                           Metric.Residuals,
                           Metric.PredictedTrue]:
                    # TODO: Do for constants.Metric.NONSCALAR_FULL_SET when
                    # all implement Metric interface
                    metric_class = mt.Metric.get_metric_class(k)
                    mean_scores[k] = metric_class.aggregate(split_results)
        return mean_scores

    def _run(self, dataset, pipeline_spec, sets_to_run=None,
             subsample_percent=None, random_state=None):
        """

        :param dataset: A dataset generated by _ClientDatasets.parse_data().
        :param pipeline_spec: A pipeline specification (obtained from the API).
        :param sets_to_run: Which experiment types to run (e.g. CV,
            train_valid, etc).
        :param subsample_percent: A multiple of 5 between 5 and 100, inclusive.
        :param random_state: int or RandomState object for random operations.
        :return: train, validation, and test scores for the experiments
            specified in sets_to_run.
        """
        assert dataset.get_task() == pipeline_spec['task']

        if sets_to_run is None:
            sets_to_run = list(TrainingType.FULL_SET)

        results = {}

        if subsample_percent is not None:
            # train on a subset of the training dataset.
            results["train_percent"] = subsample_percent
            dataset = dataset.get_subsampled_dataset(
                subsample_percent, random_state=random_state)
        else:
            results["train_percent"] = 100

        num_classes, class_labels, y_min, y_max, \
            y_std, bin_info = self._get_task_params(dataset=dataset)
        class_labels = dataset.get_class_labels()
        y_transformer = dataset.get_y_transformer()

        if TrainingType.TrainAndValidation in sets_to_run:
            # Holdout data experiment
            X_train, y_train, sample_weight_train = dataset.get_train_set()
            X_test, y_test, sample_weight_test = dataset.get_test_set()
            score_full, train_time, m, fit_model = self._run_train_valid(
                dataset, pipeline_spec)
            results['validation'] = score_full
            results['train'] = self._compute_metric(
                pipeline=m, X=X_train, y=y_train, num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                bin_info=bin_info,
                sample_weight=sample_weight_train,
                class_labels=class_labels,
                y_transformer=y_transformer)
            results['train']['train time'] = train_time

            results['test'] = self._compute_metric(
                pipeline=m, X=X_test, y=y_test, num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                bin_info=bin_info,
                sample_weight=sample_weight_test,
                class_labels=class_labels,
                y_transformer=y_transformer)

        if TrainingType.TrainFull in sets_to_run:
            # Holdout data experiment
            X_train, y_train, sample_weight_train = dataset.get_train_set()
            X_test, y_test, sample_weight_test = dataset.get_test_set()

            score_full, train_time, m, fit_model = self._run_train_full(
                dataset, pipeline_spec)

            results['train from full'] = self._compute_metric(
                pipeline=m, X=X_train, y=y_train,
                num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                sample_weight=sample_weight_train,
                class_labels=class_labels,
                y_transformer=y_transformer)
            results['train from full']['train time'] = train_time

            results['test from full'] = self._compute_metric(
                pipeline=m, X=X_test, y=y_test, num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                sample_weight=sample_weight_test,
                class_labels=class_labels,
                y_transformer=y_transformer)
            results['fit_model'] = fit_model

        if TrainingType.CrossValidation in sets_to_run or \
                TrainingType.MeanCrossValidation in sets_to_run:
            scores, fit_times, models, fit_models = self._run_cv(
                dataset, pipeline_spec)
            for i in range(len(scores)):
                score = scores[i]
                fit_time = fit_times[i]
                score['train time'] = fit_time
            results['CV'] = scores

            if TrainingType.MeanCrossValidation in sets_to_run:
                mean_scores, mean_time, models, fit_models = self._run_cv_mean(
                    dataset,
                    pipeline_spec,
                    (scores, fit_times, models))
                results['CV mean'] = mean_scores

            results['fit_model'] = fit_models

        return results

    def run(self, dataset, pipeline_spec, sets_to_run=None,
            subsample_percent=None, enforce_limits=True,
            random_state=None):
        """

        :param dataset:
        :param pipeline_spec:
        :param sets_to_run:
        :param subsample_percent:
        :param enforce_limits:
        :param random_state: int or RandomState object for random operations.
        :return:
        """
        if enforce_limits:
            return safe_enforce_limits(**self.runtime_constraints)(self._run)(
                dataset,
                pipeline_spec,
                sets_to_run,
                subsample_percent,
                random_state=random_state)
        else:
            return self._run(dataset,
                             pipeline_spec,
                             sets_to_run,
                             subsample_percent,
                             random_state=random_state)

    def run_type(self, dataset, pipeline_spec, training_type,
                 is_ensemble_iteration=False, training_percent=100,
                 subsample_seed=0):
        """

        :param dataset:
        :param pipeline_spec:
        :param training_type:
        :return:
        """

        pynobj = safe_enforce_limits(**self.runtime_constraints)

        if not is_ensemble_iteration:
            func = {
                TrainingType.TrainAndValidation: self._run_train_valid,
                TrainingType.TrainFull: self._run_train_full,
                TrainingType.CrossValidation: self._run_cv,
                TrainingType.MeanCrossValidation: self._run_cv_mean,
            }[training_type]

            if (training_percent is not None and training_percent < 100):
                dataset = dataset.get_subsampled_dataset(
                    training_percent, random_state=subsample_seed)

            result = pynobj(func)(dataset, pipeline_spec)
            return result, pynobj.exit_status
        else:
            return self.run_ensembling(dataset, pipeline_spec, training_type)

    def compute_metrics_classification_legacy(
            self, y_pred, y_test, metrics=None,
            num_classes=None, sample_weight=None):
        """

        :rtype: object
        :param y_pred:
        :param y_test:
        :param metrics:
        :param num_classes:
        :return:
        """
        if num_classes is None:
            num_classes = max(len(np.unique(y_test)))
        if metrics is None:
            metrics = mt.get_default_metrics(task="classification")

        if num_classes is None:
            num_classes = max(len(np.unique(y_test)), len(np.unique(y_pred)))

        results = {}
        if 'AUC_macro' in metrics or 'AUC_weighted' in metrics:
            binarizer = sklearn.preprocessing.LabelBinarizer()
            binarizer.fit(y_test)
            y_test_bin = binarizer.transform(y_test)
            y_pred_bin = binarizer.transform(y_pred)
            results['AUC_macro'] = sklearn.metrics.roc_auc_score(
                y_test_bin, y_pred_bin, average='macro',
                sample_weight=sample_weight)
            results['AUC_weighted'] = sklearn.metrics.roc_auc_score(
                y_test_bin, y_pred_bin, average='weighted',
                sample_weight=sample_weight)
        if "accuracy" in metrics:
            results['accuracy'] = sklearn.metrics.accuracy_score(
                y_test, y_pred, sample_weight=sample_weight)
        if "weighted_accuracy" in metrics:
            # accuracy weighted by number of elements for each class
            w = np.ones(y_test.shape[0])
            for idx, i in enumerate(np.bincount(y_test.ravel())):
                w[y_test.ravel() == idx] *= \
                    (i / float(y_test.ravel().shape[0]))
            results['weighted_accuracy'] = sklearn.metrics.accuracy_score(
                y_test, y_pred, sample_weight=w)
        if "norm_macro_recall" in metrics:
            # this is what is used here
            # https://github.com/ch-imad/AutoMl_Challenge/blob/2353ec0/
            # Starting_kit/scoring_program/libscores.py#L187
            # for the AutoML challenge https://competitions.codalab.org/
            # competitions/2321#learn_the_details-evaluation
            # This is a normalized macro averaged recall, rather than accuracy
            # https://github.com/scikit-learn/scikit-learn/issues/6747#issuecomment-217587210
            # Random performance is 0.0 perfect performance is 1.0
            confusion_matrix = sklearn.metrics.confusion_matrix(
                y_test, y_pred, sample_weight=sample_weight)
            r = 1 / num_classes
            results['norm_macro_recall'] = (
                np.mean(confusion_matrix.diagonal() /
                        confusion_matrix.sum(axis=1)) - r) / (1 - r)
        if "balanced_accuracy" in metrics:
            classes = np.unique(y_test)
            bac = np.mean([sklearn.metrics.roc_auc_score(
                y_test == k, y_pred == k, sample_weight=sample_weight)
                for k in classes])
            results['balanced_accuracy'] = bac
        # for the new metrics not in the legacy list and each metric to the
        # result to make it compatable.
        for metric in metrics:
            if metric not in results:
                results[metric] = np.nan

        return results

    def run_ensembling(self, dataset, pipeline, training_type):
        """
        Runs the ensemble selection & generates an
        Estimator out of the chosen pipelines

        Arguments:
            dataset -- The input dataset which is used for the ensemble
                        selection
            pipeline {Pipeline} -- The Ensemble pipeline to fit
            training_type {constants.TrainingType} -- The type of training
                        used.
        """
        # disable safe_enforce_limits until LightGBM hanging bug is fixed
        # pynobj = safe_enforce_limits(**self.runtime_constraints)
        result = self._run_ensembling_internal(dataset,
                                               pipeline,
                                               training_type)
        return result, 0

    def _run_ensembling_internal(self, dataset, pipeline, training_type):
        num_classes, class_labels, y_min, y_max, \
            y_std, bin_info = self._get_task_params(dataset=dataset)
        y_transformer = dataset.get_y_transformer()

        fit_time, fitted_ensemble_model, cross_validated_ensembles = \
            self.time_fit_ensemble(pipeline, training_type, dataset)
        fitted_pipeline = make_pipeline(fitted_ensemble_model)

        if training_type == TrainingType.TrainAndValidation:
            X_valid, y_valid, sample_weight_valid = dataset.get_valid_set()
            score_valid = self._compute_metric(
                pipeline=fitted_pipeline, X=X_valid, y=y_valid,
                num_classes=num_classes,
                y_min=y_min, y_max=y_max, y_std=y_std,
                sample_weight=sample_weight_valid,
                bin_info=bin_info,
                class_labels=class_labels,
                y_transformer=y_transformer)
        elif training_type == TrainingType.MeanCrossValidation:
            fold_index = 0
            scores = []
            for X_train, y_train, sample_wt_train, X_test,\
                    y_test, sample_wt_test in dataset.get_CV_splits():
                m = cross_validated_ensembles[fold_index]
                score = self._compute_metric(
                    pipeline=m, X=X_test, y=y_test, num_classes=num_classes,
                    y_min=y_min, y_max=y_max, y_std=y_std,
                    sample_weight=sample_wt_test,
                    bin_info=bin_info,
                    class_labels=class_labels,
                    y_transformer=y_transformer)
                scores.append(score)
                fold_index += 1
            score_valid = self._get_mean_cv_scores(scores)
        return score_valid, fit_time, pipeline, fitted_pipeline


if __name__ == '__main__':
    pass
