# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Computation of available metrics."""
import copy
import sys

import numpy as np
import scipy.stats as st
import sklearn.metrics
import sklearn.preprocessing

from automl.client.core.common import constants


def minimize_or_maximize(metric, task=None):
    """Selects the objective given a metric
    Some metrics should be minimized and some should be maximized
    :param metric: the name of the metric to look up
    :param task: one of constants.Tasks.
    :return: returns one of constants.OptimizerObjectives.
    """
    if task is None:
        reg_metrics = get_default_metric_with_objective(
            constants.Tasks.REGRESSION)
        class_metrics = get_default_metric_with_objective(
            constants.Tasks.CLASSIFICATION)
        if metric in reg_metrics:
            task = constants.Tasks.REGRESSION
        elif metric in class_metrics:
            task = constants.Tasks.CLASSIFICATION
        else:
            msg = 'Could not find objective for metric "{0}"'.format(metric)
            raise ValueError(msg)
    return get_default_metric_with_objective(task)[metric]


def get_all_nan(task):
    """Creates a dictionary of metrics to values for the given task
    All metric values are set to nan initially
    :param task: one of constants.Tasks.
    :return: returns a dictionary of nans for each metric for the task.
    """
    metrics = get_default_metric_with_objective(task)
    return {m: np.nan for m in metrics}


def get_metric_ranges(task, for_assert_sane=False):
    minimums = get_min_values(task)
    maximums = get_max_values(task, for_assert_sane=for_assert_sane)
    return minimums, maximums


def get_worst_values(task, for_assert_sane=False):
    minimums, maximums = get_metric_ranges(
        task, for_assert_sane=for_assert_sane)
    metrics = get_default_metric_with_objective(task)
    _MAX = constants.OptimizerObjectives.MAXIMIZE
    bad = {m: minimums[m] if obj == _MAX else maximums[m]
           for m, obj in metrics.items()}
    return bad


def get_min_values(task):
    metrics = get_default_metric_with_objective(task)
    # 0 is the minimum for metrics that are minimized and maximized
    bad = {m: 0.0 for m, obj in metrics.items()}
    bad[constants.Metric.R2Score] = -10.0  # R2 is different, clipped to -10.0
    bad[constants.Metric.Spearman] = -1.0
    return bad


def get_max_values(task, for_assert_sane=False):
    metrics = get_default_metric_with_objective(task)
    _MAX = constants.OptimizerObjectives.MAXIMIZE
    bad = {m: 1.0 if obj == _MAX else sys.float_info.max
           for m, obj in metrics.items()}
    # so the assertions don't fail, could also clip metrics instead
    if not for_assert_sane:
        bad[constants.Metric.LogLoss] = 10.0
        bad[constants.Metric.NormRMSE] = 10.0
        bad[constants.Metric.NormRMSLE] = 10.0
        bad[constants.Metric.NormMeanAbsError] = 10.0
        bad[constants.Metric.NormMedianAbsError] = 10.0
    return bad


def assert_metrics_sane(metrics, task):
    """Asserts that the given metric values are same
    The metric values should not be worse than the worst possible values
    for those metrics given the objectives for those metrics
    :param task: string "classification" or "regression"
    """
    worst = get_worst_values(task, for_assert_sane=True)
    obj = get_default_metric_with_objective(task)
    for k, v in metrics.items():
        if not np.isscalar(v) or np.isnan(v):
            continue
        # This seems to vary a lot.
        if k == constants.Metric.ExplainedVariance:
            continue
        if obj[k] == constants.OptimizerObjectives.MAXIMIZE:
            assert v >= worst[k], (
                '{0} is not worse than {1} for metric {2}'.format(
                    worst[k], v, k))
        else:
            assert v <= worst[k], (
                '{0} is not worse than {1} for metric {2}'.format(
                    worst[k], v, k))


def get_default_metric_with_objective(task):
    """Gets the dictionary of metric -> objective for the given task
    :param task: string "classification" or "regression"
    :return: dictionary of metric -> objective
    """
    if task == constants.Tasks.CLASSIFICATION:
        return constants.MetricObjective.Classification
    elif task == constants.Tasks.REGRESSION:
        return constants.MetricObjective.Regression
    else:
        raise NotImplementedError


def get_scalar_metrics(task):
    """Gets the scalar metrics supported for a given task
    :param task: string "classification" or "regression"
    :return: a list of the default metrics supported for the task
    """
    if task == constants.Tasks.CLASSIFICATION:
        return list(constants.Metric.SCALAR_CLASSIFICATION_SET)
    elif task == constants.Tasks.REGRESSION:
        return list(constants.Metric.SCALAR_REGRESSION_SET)
    else:
        raise NotImplementedError


def get_default_metrics(task):
    """Gets the metrics supported for a given task as a list
    :param task: string "classification" or "regression"
    :return: a list of the default metrics supported for the task
    """
    if task == constants.Tasks.CLASSIFICATION:
        return constants.Metric.CLASSIFICATION_SET
    elif task == constants.Tasks.REGRESSION:
        return constants.Metric.REGRESSION_SET
    else:
        raise NotImplementedError


def add_padding_for_missing_class_labels(pred_proba_result, trained_class_labels, class_labels):
    """Adds padding to the predicted probabilities for missing class labels.
    For the case when a model was trained on less classes than what the dataset contains
    we'll add corresponding columns to predict_proba result with 0 probability.

    :param pred_proba_result: predicted value (in probability in case of classification)
    :param trained_class_labels: the class labels detected by the trained model
    :param class_labels: the class labels detected from the entire dataset
    :return: predicted probabilities
    """
    if trained_class_labels is not None and \
            class_labels is not None and \
            len(trained_class_labels) != len(class_labels):
        # in case the classifier was trained on less class labels than what the dataset contains,
        # we need to iterate through all the dataset classes and when we see a gap in the predictions
        # we'll have to insert an empty column with probability 0
        trained_class_labels_clone = copy.deepcopy(trained_class_labels)
        # we'll iterate through the dataset classes with the following index
        dataset_class_index = 0
        # we'll iterate through this model's classes with the following index
        model_class_index = 0
        dataset_class_number = len(class_labels)
        while len(trained_class_labels_clone) != dataset_class_number:
            expected_dataset_class = class_labels[dataset_class_index]
            # if the classes match we increment both indices
            if model_class_index < len(trained_class_labels_clone) and expected_dataset_class == \
                    trained_class_labels_clone[model_class_index]:
                model_class_index += 1
                dataset_class_index += 1
            else:
                # otherwise, we'll have to add the expected class and it's corresponding probabilities set to 0
                pred_proba_result = np.insert(pred_proba_result,
                                              model_class_index,
                                              np.zeros((pred_proba_result.shape[0],)),
                                              axis=1)
                trained_class_labels_clone = np.insert(trained_class_labels_clone,
                                                       model_class_index,
                                                       expected_dataset_class)
        if not np.array_equal(trained_class_labels_clone, class_labels):
            raise ValueError("The padding of trained model classes resulted in an inconsistency. ({}) vs ({})".
                             format(trained_class_labels_clone, class_labels))
    return pred_proba_result


def compute_metrics(y_pred,
                    y_test,
                    metrics=None,
                    task=constants.Tasks.CLASSIFICATION,
                    sample_weight=None,
                    num_classes=None,
                    class_labels=None,
                    trained_class_labels=None,
                    y_transformer=None,
                    y_max=None, y_min=None, y_std=None,
                    bin_info=None):
    """Computes the metrics given the test data results
    :param y_pred: predicted value (in probability in case of classification)
    :param y_test: target value
    :param metrics: metric/metrics to compute
    :param num_classes: num of classes for classification task
    :param class_labels: labels for classification task
    :param trained_class_labels: labels for classification task as identified by the trained model
    :param task: ml task
    :param y_max: max target value for regression task
    :param y_min: min target value for regression task
    :param y_std: standard deviation of regression targets
    :param sample_weight: weights for samples in dataset
    :return: returns a dictionary with metrics computed
    """

    if metrics is None:
        metrics = get_default_metrics(task)

    if task == constants.Tasks.CLASSIFICATION:
        return compute_metrics_classification(y_pred, y_test, metrics,
                                              num_classes=num_classes,
                                              sample_weight=sample_weight,
                                              class_labels=class_labels,
                                              trained_class_labels=trained_class_labels,
                                              y_transformer=y_transformer)
    elif task == constants.Tasks.REGRESSION:
        return compute_metrics_regression(y_pred, y_test, metrics,
                                          y_max, y_min, y_std,
                                          sample_weight=sample_weight,
                                          bin_info=bin_info)
    else:
        raise NotImplementedError


def compute_metrics_classification(y_pred_probs, y_test, metrics,
                                   num_classes=None, sample_weight=None,
                                   class_labels=None, trained_class_labels=None, y_transformer=None):
    """
    Computes the metrics for a classification task. All class labels for y should come
    as seen by the fitted model (i.e. if the fitted model uses a y transformer the labels
    should also come transformed).

    All metrics present in `metrics` will be present in the output dictionary with either
    the value(s) calculated or `nan` if metrics
    calculation failed.

    :param y_pred_probs: The probability predictions.
    :param y_test: The target value. Transformed if using a y transformer.
    :param metrics: metric/metrics to compute
    :type metrics: list
    :param class_labels:
        Labels for classification task. This should be the entire y label set. These should
         be transformed if using a y transformer. Required for all non-scalars to be calculated.
    :param trained_class_labels:
        Labels for classification task as seen (trained on) by the
        trained model. Required when training set did not see all classes from full set.
    :param num_classes: Number of classes in the entire y set. Required for all metrics.
    :param sample_weight:
        The sample weight to be used on metrics calculation. This does not need
        to match sample weights on the fitted model.
    :param y_transformer: Used to inverse transform labels from `y_test`. Required for non-scalar metrics.
    :return: A dictionary with metrics computed.
    """
    if y_test.dtype == np.float32 or y_test.dtype == np.float64:
        # Assume that the task is set appropriately and that the data
        # just had a float label arbitrarily.
        y_test = y_test.astype(np.int64)

    # Some metrics use an eps of 1e-15 by default, which results in nans
    # for float32.
    if y_pred_probs.dtype == np.float32:
        y_pred_probs = y_pred_probs.astype(np.float64)

    if num_classes is None:
        num_classes = max(len(np.unique(y_test)), y_pred_probs.shape[1])

    if metrics is None:
        metrics = get_default_metrics(constants.Tasks.CLASSIFICATION)

    y_test = np.ravel(y_test)

    results = {}

    binarizer = sklearn.preprocessing.LabelBinarizer()

    if class_labels is not None:
        binarizer.fit(class_labels)
    else:
        binarizer.fit(y_test)

    y_test_bin = binarizer.transform(y_test)

    # we need to make sure that we have probabilities from all classes in the dataset
    # in case the trained model wasn't fitted on the entire set of class labels
    y_pred_probs = add_padding_for_missing_class_labels(y_pred_probs,
                                                        trained_class_labels,
                                                        class_labels)

    y_pred_probs_full = y_pred_probs
    y_pred_bin = np.argmax(y_pred_probs_full, axis=1)

    if class_labels is not None:
        y_pred_bin = class_labels[y_pred_bin]

    if num_classes is None:
        num_classes = max(len(np.unique(y_test)), len(np.unique(y_pred_bin)))

    if num_classes == 2:
        # if both classes probs are passed, pick the positive class probs as
        # binarizer only outputs single column
        y_pred_probs = y_pred_probs[:, 1]

    # For accuracy table and confusion matrix,
    # the y_test_original is used to keep label consistency.
    # For other metrics, the y_test is passed.
    y_test_original = y_test
    if class_labels is not None:
        class_labels_original = class_labels
    if y_transformer is not None:
        y_test_original = y_transformer.inverse_transform(y_test_original)
        if class_labels is not None:
            class_labels_original = y_transformer.inverse_transform(class_labels_original)

    if constants.Metric.Accuracy in metrics:
        results[constants.Metric.Accuracy] = try_calculate_metric(
            score=sklearn.metrics.accuracy_score, y_true=y_test,
            y_pred=y_pred_bin, sample_weight=sample_weight)

    if constants.Metric.WeightedAccuracy in metrics:
        # accuracy weighted by number of elements for each class
        w = np.ones(y_test.shape[0])
        for idx, i in enumerate(np.bincount(y_test.ravel())):
            w[y_test.ravel() == idx] *= (i / float(y_test.ravel().shape[0]))
        results[constants.Metric.WeightedAccuracy] = try_calculate_metric(
            score=sklearn.metrics.accuracy_score,
            y_true=y_test,
            y_pred=y_pred_bin,
            sample_weight=w)

    if constants.Metric.NormMacroRecall in metrics:
        # this is what is used here
        # https://github.com/ch-imad/AutoMl_Challenge/blob/2353ec0
        # /Starting_kit/scoring_program/libscores.py#L187
        # for the AutoML challenge
        # https://competitions.codalab.org/competitions/2321
        # #learn_the_details-evaluation
        # This is a normalized macro averaged recall, rather than accuracy
        # https://github.com/scikit-learn/scikit-learn/issues/6747
        # #issuecomment-217587210
        # Random performance is 0.0 perfect performance is 1.0
        cmat = try_calculate_metric(
            sklearn.metrics.confusion_matrix, y_true=y_test,
            y_pred=y_pred_bin, sample_weight=sample_weight)
        if isinstance(cmat, float):
            results[constants.Metric.NormMacroRecall] = \
                constants.Defaults.DEFAULT_PIPELINE_SCORE
        else:
            R = 1 / num_classes
            cms = cmat.sum(axis=1)
            if cms.sum() == 0:
                results[constants.Metric.NormMacroRecall] = \
                    constants.Defaults.DEFAULT_PIPELINE_SCORE
            else:
                results[constants.Metric.NormMacroRecall] = max(
                    0.0,
                    (np.mean(cmat.diagonal() / cmat.sum(axis=1)) - R) /
                    (1 - R))

    if constants.Metric.LogLoss in metrics:
        results[constants.Metric.LogLoss] = \
            try_calculate_metric(sklearn.metrics.log_loss, y_true=y_test,
                                 y_pred=y_pred_probs,
                                 labels=np.arange(0, num_classes),
                                 sample_weight=sample_weight)

    for name in metrics:
        # TODO: Remove this conditional once all metrics implement
        # the Metric interface for compute and aggregate
        # Compute should take dataset
        if name in [constants.Metric.AccuracyTable,
                    constants.Metric.ConfusionMatrix]:
            try:
                metric_class = Metric.get_metric_class(name)
                metric = metric_class(y_test_original, y_pred_probs_full)
                score = metric.compute(sample_weights=sample_weight,
                                       class_labels=class_labels_original)
                results[name] = score
            except Exception as e:
                results[name] = np.nan

    for m in metrics:
        if 'AUC' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.roc_auc_score, y_true=y_test_bin,
                y_score=y_pred_probs, average=m.replace('AUC_', ''),
                sample_weight=sample_weight)

        if 'f1_score' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.f1_score, y_true=y_test, y_pred=y_pred_bin,
                average=m.replace('f1_score_', ''),
                sample_weight=sample_weight)

        if 'precision_score' in m and 'average' not in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.precision_score,
                y_true=y_test, y_pred=y_pred_bin,
                average=m.replace('precision_score_', ''),
                sample_weight=sample_weight)

        if 'recall_score' in m or m == constants.Metric.BalancedAccuracy:
            if 'recall_score' in m:
                average_modifier = m.replace('recall_score_', '')
            elif m == constants.Metric.BalancedAccuracy:
                average_modifier = 'macro'
            results[m] = try_calculate_metric(
                sklearn.metrics.recall_score,
                y_true=y_test,
                y_pred=y_pred_bin,
                average=average_modifier,
                sample_weight=sample_weight)

        if 'average_precision_score' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.average_precision_score,
                y_true=y_test_bin,
                y_score=y_pred_probs,
                average=m.replace('average_precision_score_', ''),
                sample_weight=sample_weight)

    assert_metrics_sane(results, constants.Tasks.CLASSIFICATION)
    return results


def compute_mean_cv_scores(scores, metrics):
    means = {}
    for name in metrics:
        if name in scores[0]:
            split_results = [score[name] for score in scores if name in score]
            if name in constants.Metric.SCALAR_FULL_SET:
                means[name] = float(np.mean(split_results))
            elif name in constants.Metric.NONSCALAR_FULL_SET:
                metric_class = Metric.get_metric_class(name)
                means[name] = metric_class.aggregate(split_results)

    train_type = constants.TrainingResultsType.TRAIN_TIME
    train_times = [res[train_type] for res in scores if train_type in res]
    if train_times:
        means[train_type] = float(np.mean(train_times))

    return means


def try_calculate_metric(score, **karg):
    """Calculates the metric given a metric calculation function
    :param score: an sklearn metric calculation function to score
    :return: the calculated score (or nan if there was an exception)
    """
    try:
        return score(**karg)
    except Exception as e:
        return constants.Defaults.DEFAULT_PIPELINE_SCORE


def reformat_table(dictionary, yaxis, xaxis):
    """Convert x and y axis lists to a dictionary"""
    reformated_dict = dict()
    for label in dictionary[yaxis]:
        ykey, xkey = yaxis + '_' + str(label), xaxis + '_' + str(label)
        reformated_dict[xkey] = dictionary[xaxis][label]
        reformated_dict[ykey] = dictionary[yaxis][label]
    return reformated_dict


def compute_metrics_regression(y_pred, y_test, metrics,
                               y_max=None,
                               y_min=None,
                               y_std=None,
                               sample_weight=None,
                               bin_info=None):
    """
    Computes the metrics for a regression task.

    `y_max`, `y_min`, and `y_std` should be based on `y_test` information unless
    you would like to compute multiple metrics for comparison (ex. cross validation),
    in which case, you should use a common range and standard deviation. You may
    also pass in `y_max`, `y_min`, and `y_std` if you do not want it to be calculated.

    All metrics present in `metrics` will be present in the output dictionary with either
    the value(s) calculated or `nan` if metric calculation failed.

    :param y_pred: The predict values.
    :param y_test: The target values.
    :param metrics: List of metric names for metrics to calculate.
    :type metrics: list
    :param y_max: The max target value.
    :param y_min: The min target value.
    :param y_std: The standard deviation of targets value.
    :param sample_weight:
        The sample weight to be used on metrics calculation. This does not need
        to match sample weights on the fitted model.
    :param bin_info:
        The binning information for true values. This should be calculated from
        :class:`ClientDatasets` :func:`make_bin_info`. Required for calculating
        non-scalar metrics.
    :return: A dictionary with metrics computed.
    """
    if y_min is None:
        y_min = np.min(y_test)
    if y_max is None:
        y_max = np.max(y_test)
        assert y_max > y_min
    if y_std is None:
        y_std = np.std(y_test)

    if metrics is None:
        metrics = get_default_metrics(constants.Tasks.REGRESSION)

    results = {}

    # Regression metrics The scale of some of the metrics below depends on the
    # scale of the data. For this reason, we rescale it by the distance between
    # y_max and y_min. Since this can produce negative values we take the abs
    # of the distance https://en.wikipedia.org/wiki/Root-mean-square_deviation

    if constants.Metric.ExplainedVariance in metrics:
        bac = sklearn.metrics.explained_variance_score(
            y_test, y_pred, sample_weight=sample_weight,
            multioutput='uniform_average')
        results[constants.Metric.ExplainedVariance] = bac

    if constants.Metric.R2Score in metrics:
        bac = sklearn.metrics.r2_score(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        results[constants.Metric.R2Score] = np.clip(
            bac, constants.Metric.CLIPS_NEG[constants.Metric.R2Score], 1.0)

    if constants.Metric.Spearman in metrics:
        bac = st.spearmanr(y_test, y_pred)[0]
        results[constants.Metric.Spearman] = bac

        # mean AE
    if constants.Metric.MeanAbsError in metrics:
        bac = sklearn.metrics.mean_absolute_error(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        results[constants.Metric.MeanAbsError] = bac

    if constants.Metric.NormMeanAbsError in metrics:
        bac = sklearn.metrics.mean_absolute_error(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormMeanAbsError] = bac

    # median AE
    if constants.Metric.MedianAbsError in metrics:
        bac = sklearn.metrics.median_absolute_error(y_test, y_pred)
        results[constants.Metric.MedianAbsError] = bac

    if constants.Metric.NormMedianAbsError in metrics:
        bac = sklearn.metrics.median_absolute_error(y_test, y_pred)
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormMedianAbsError] = bac

    # RMSE
    if constants.Metric.RMSE in metrics:
        bac = np.sqrt(
            sklearn.metrics.mean_squared_error(
                y_test, y_pred, sample_weight=sample_weight,
                multioutput='uniform_average'))
        results[constants.Metric.RMSE] = bac

    if constants.Metric.NormRMSE in metrics:
        bac = np.sqrt(
            sklearn.metrics.mean_squared_error(
                y_test, y_pred, sample_weight=sample_weight,
                multioutput='uniform_average'))
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormRMSE] = np.clip(
            bac, 0,
            constants.Metric.CLIPS_POS.get(constants.Metric.NormRMSE, 100))

    # RMSLE
    if constants.Metric.RMSLE in metrics:
        bac = None
        try:
            bac = np.sqrt(
                sklearn.metrics.mean_squared_log_error(
                    y_test, y_pred, sample_weight=sample_weight,
                    multioutput='uniform_average')
            )
            bac = np.clip(
                bac, 0,
                constants.Metric.CLIPS_POS.get(constants.Metric.RMSLE, 100))
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.RMSLE] = bac

    if constants.Metric.NormRMSLE in metrics:
        bac = None
        try:
            bac = np.sqrt(
                sklearn.metrics.mean_squared_log_error(
                    y_test, y_pred, sample_weight=sample_weight,
                    multioutput='uniform_average'))
            bac = bac / np.abs(np.log1p(y_max) - np.log1p(y_min))
            bac = np.clip(
                bac, 0,
                constants.Metric.CLIPS_POS.get(
                    constants.Metric.NormRMSLE, 100))
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.NormRMSLE] = bac

    for name in metrics:
        # TODO: Remove this conditional once all metrics implement
        # the Metric interface for compute and aggregate
        # Compute should take dataset
        if name in [constants.Metric.Residuals,
                    constants.Metric.PredictedTrue]:
            try:
                metric_class = Metric.get_metric_class(name)
                metric = metric_class(y_test, y_pred)
                results[name] = metric.compute(bin_info=bin_info,
                                               y_std=y_std)
            except Exception as e:
                results[name] = np.nan

    assert_metrics_sane(results, constants.Tasks.REGRESSION)
    return results


def _predvstrue_compute(y_test, y_pred, bin_info):
    num_bins = bin_info['number_of_bins']
    pred_indices_per_bin = [np.array([], dtype=int)] * (num_bins)
    predvtruedict = {
        constants.Preds_Reg.TRUE_VALS_BINS_START:
        bin_info['bin_starts'],
        constants.Preds_Reg.TRUE_VALS_BINS_END:
        bin_info['bin_ends'],
        constants.Preds_Reg.AVG_PRED_VALS_PER_BIN:
        np.zeros(num_bins),
        constants.Preds_Reg.PRED_ERROR_PER_BIN:
        np.zeros(num_bins),
        constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN:
        np.zeros(num_bins)}
    for i in range(len(y_test)):
        for bin_index in range(len(bin_info['bin_ends'])):
            if y_test[i] <= bin_info['bin_ends'][bin_index]:
                pred_indices_per_bin[bin_index] = np.append(
                    pred_indices_per_bin[bin_index], int(i))
                break
    predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN] = \
        np.array([len(x) for x in pred_indices_per_bin])
    predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN] = \
        np.array([
            np.mean(y_pred[x])
            if len(x) != 0
            else 0 for x in pred_indices_per_bin])
    predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN] = \
        np.array([np.std(y_pred[x])
                  if len(x) != 0 else 0
                  for x in pred_indices_per_bin])
    return predvtruedict


def _predvstrue_mean(dicts):
    num_cv, tot_bin_count = len(dicts), \
        len(dicts[0][
            constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN])
    predvtruedict = {
        constants.Preds_Reg.TRUE_VALS_BINS_START: np.zeros(tot_bin_count),
        constants.Preds_Reg.TRUE_VALS_BINS_END: np.zeros(tot_bin_count),
        constants.Preds_Reg.AVG_PRED_VALS_PER_BIN: np.zeros(tot_bin_count),
        constants.Preds_Reg.PRED_ERROR_PER_BIN: np.zeros(tot_bin_count),
        constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN: np.zeros(tot_bin_count)}
    for i in range(tot_bin_count):
        predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] = \
            np.sum(np.array(
                [dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]
                 for j in range(num_cv)]))
        if predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] != 0:
            weighted_means_sum = np.sum(np.array(
                [dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] *
                 dicts[j][constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i]
                 for j in range(num_cv)]))
            predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] = \
                weighted_means_sum \
                / predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]
            std_devs = np.sum(np.array([(
                dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] *
                (dicts[j][constants.Preds_Reg.PRED_ERROR_PER_BIN][i] ** 2 +
                 (dicts[j][constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] -
                  predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][
                      i]) **
                 2)
            ) for j in range(num_cv)]))

            predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN][i] = \
                ((std_devs) / predvtruedict[
                    constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]) ** (0.5)
        else:
            predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] = 0
            predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN][i] = 0
    predvtruedict[constants.Preds_Reg.TRUE_VALS_BINS_START] = \
        dicts[0][constants.Preds_Reg.TRUE_VALS_BINS_START]
    predvtruedict[constants.Preds_Reg.TRUE_VALS_BINS_END] = \
        dicts[0][constants.Preds_Reg.TRUE_VALS_BINS_END]
    return predvtruedict


class Metric:
    """Abstract class for all metrics"""

    SCHEMA_TYPE = 'schema_type'
    SCHEMA_VERSION = 'schema_version'
    DATA = 'data'

    def __init__(self, y, y_pred):
        if y.shape[0] != y_pred.shape[0]:
            raise ValueError("Mismatched input shapes: y={}, y_pred={}"
                             .format(y.shape, y_pred.shape))
        self._y = y
        self._y_pred = y_pred
        self._data = {}

    @staticmethod
    def aggregate(scores):
        """Folds several scores from a computed metric together
        :param scores: a list of computed scores
        :return: the aggregated scores
        """
        raise NotImplementedError

    @staticmethod
    def _data_to_dict(schema_type, schema_version, data):
        return {
            Metric.SCHEMA_TYPE: schema_type,
            Metric.SCHEMA_VERSION: schema_version,
            Metric.DATA: data
        }

    @staticmethod
    def get_metric_class(metric_name):
        """Returns the metric class based on the constant name of the metric
        :param metric: the constant name of the metric
        :return: the class of the metric
        """
        class_map = {
            constants.Metric.AccuracyTable: AccuracyTableMetric,
            constants.Metric.ConfusionMatrix: ConfusionMatrixMetric,
            constants.Metric.Residuals: ResidualsMetric,
            constants.Metric.PredictedTrue: PredictedTrueMetric
        }
        if metric_name not in class_map:
            raise ValueError("Metric class {} was not found in \
                              Metric.get_metric_class".format(metric_name))
        return class_map[metric_name]

    @staticmethod
    def _make_json_safe(o):
        make_safe = Metric._make_json_safe
        scalar_types = [int, float, str, type(None)]
        if type(o) in scalar_types:
            return o
        elif isinstance(o, dict):
            return {k: make_safe(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [make_safe(v) for v in o]
        elif isinstance(o, tuple):
            return tuple(make_safe(v) for v in o)
        elif isinstance(o, np.ndarray):
            return make_safe(o.tolist())
        else:
            raise ValueError("Cannot encode type {}".format(type(o)))


class ClassificationMetric(Metric):
    """Abstract class for classification metrics"""

    def compute(self, sample_weights=None, class_labels=None):
        """Computes the metric
        :param sample_weights: the weighting of each sample in the calculation
        :param class_labels: the labels for the classes in the dataset
        :return: the computed metric
        """
        raise NotImplementedError


class RegressionMetric(Metric):
    """Abstract class for classification metrics"""

    def compute(self, sample_weights=None, bin_info=None,
                y_min=None, y_max=None, y_std=None):
        """Computes the metric
        :param sample_weights: the weighting of each sample in the calculation
        :param bin_info: metadata about the dataset needed to compute bins
            for some metrics
        :param y_min: the minimum target value
        :param y_max: the maximum target value
        :param y_std: the standard deviation of targets
        :return: the computed metric
        """
        raise NotImplementedError


class AccuracyTableMetric(ClassificationMetric):
    """Accuracy Table Metric"""

    SCHEMA_TYPE = constants.Metric.SCHEMA_TYPE_ACCURACY_TABLE
    SCHEMA_VERSION = 'v1'

    NUM_POINTS = 100

    PROB_TABLES = 'probability_tables'
    PERC_TABLES = 'percentile_tables'
    PROB_THOLDS = 'probability_thresholds'
    PERC_THOLDS = 'percentile_thresholds'
    CLASS_LABELS = 'class_labels'

    @staticmethod
    def _data_to_dict(data):
        schema_type = AccuracyTableMetric.SCHEMA_TYPE
        schema_version = AccuracyTableMetric.SCHEMA_VERSION
        return super(AccuracyTableMetric, AccuracyTableMetric)\
            ._data_to_dict(schema_type, schema_version, data)

    def _build_tables(self, class_labels):
        """
        Builds tables and thresholds for probability and
        percentile threshold spacing
        """
        y_labels = np.unique(self._y)
        y_label_map = {l: idx for idx, l in enumerate(y_labels)}
        y_indices = [y_label_map[v] for v in self._y]
        y_bin = np.eye(len(y_labels), dtype=int)[y_indices]
        data = zip(y_bin.T, self._y_pred.T)

        prob_tables, perc_tables = [], []
        num_points = AccuracyTableMetric.NUM_POINTS
        prob_thresholds = np.linspace(0, 1, num_points)
        percs = prob_thresholds * 100

        for c_y_bin, c_y_pred in data:
            perc_thresholds = np.percentile(c_y_pred, percs)
            prob_table = self._create_class_samples(c_y_bin, c_y_pred,
                                                    prob_thresholds)
            perc_table = self._create_class_samples(c_y_bin, c_y_pred,
                                                    perc_thresholds)
            prob_tables.append(prob_table)
            perc_tables.append(perc_table)

        # Add missing tables from classes not included in training data
        full_prob, full_perc = self._include_missing_labels(class_labels,
                                                            prob_tables,
                                                            perc_tables,
                                                            y_label_map)
        self._data[AccuracyTableMetric.PROB_TABLES] = full_prob
        self._data[AccuracyTableMetric.PERC_TABLES] = full_perc
        self._data[AccuracyTableMetric.PROB_THOLDS] = prob_thresholds
        self._data[AccuracyTableMetric.PERC_THOLDS] = percs

    def _include_missing_labels(self, class_labels, prob_tables,
                                perc_tables, y_label_map):
        full_prob_tables, full_perc_tables = [], []
        for class_label in class_labels:
            if class_label in y_label_map:
                y_index = y_label_map[class_label]
                full_prob_tables.append(prob_tables[y_index])
                full_perc_tables.append(perc_tables[y_index])
            else:
                empty_table = np.zeros((len(self._y), 4), dtype=int)
                full_prob_tables.append(empty_table)
                full_perc_tables.append(empty_table)
        return full_prob_tables, full_perc_tables

    def _create_class_samples(self, class_y_bin, class_y_pred, thresholds):
        """Calculates the confusion values at all thresholds for one class"""
        table = []
        num_positive = np.sum(class_y_bin)
        num_samples = class_y_bin.size
        for threshold in thresholds:
            under_threshold = class_y_bin[class_y_pred < threshold]
            fn = np.sum(under_threshold)
            tn = under_threshold.size - fn
            tp, fp = num_positive - fn, num_samples - num_positive - tn
            conf_values = np.array([tp, fp, tn, fn], dtype=int)
            table.append(conf_values)
        return table

    def compute(self, sample_weights=None, class_labels=None):
        """Computes the score for the metric"""
        if class_labels is None:
            raise ValueError("Class labels required to compute AccuracyTable")
        string_labels = [str(label) for label in class_labels]
        self._data[AccuracyTableMetric.CLASS_LABELS] = string_labels
        self._build_tables(class_labels)
        ret = AccuracyTableMetric._data_to_dict(self._data)
        return Metric._make_json_safe(ret)

    @staticmethod
    def aggregate(scores):
        """Folds several scores from a computed metric together
        :param scores: a list of computed scores
        :return: the aggregated scores
        """
        if len(scores) == 0:
            raise ValueError("Scores must not be empty to aggregate")
        score_data = [score[Metric.DATA] for score in scores]
        prob_tables = [d[AccuracyTableMetric.PROB_TABLES] for d in score_data]
        perc_tables = [d[AccuracyTableMetric.PERC_TABLES] for d in score_data]
        data_agg = {
            AccuracyTableMetric.PROB_TABLES: (
                np.sum(prob_tables, axis=0)),
            AccuracyTableMetric.PERC_TABLES: (
                np.sum(perc_tables, axis=0)),
            AccuracyTableMetric.PROB_THOLDS: (
                score_data[0][AccuracyTableMetric.PROB_THOLDS]),
            AccuracyTableMetric.PERC_THOLDS: (
                score_data[0][AccuracyTableMetric.PERC_THOLDS]),
            AccuracyTableMetric.CLASS_LABELS: (
                score_data[0][AccuracyTableMetric.CLASS_LABELS])
        }
        ret = AccuracyTableMetric._data_to_dict(data_agg)
        return Metric._make_json_safe(ret)


class ConfusionMatrixMetric(ClassificationMetric):
    """Confusion Matrix Metric"""

    SCHEMA_TYPE = constants.Metric.SCHEMA_TYPE_CONFUSION_MATRIX
    SCHEMA_VERSION = 'v1'

    MATRIX = 'matrix'
    CLASS_LABELS = 'class_labels'

    @staticmethod
    def _data_to_dict(data):
        schema_type = ConfusionMatrixMetric.SCHEMA_TYPE
        schema_version = ConfusionMatrixMetric.SCHEMA_VERSION
        return Metric._data_to_dict(schema_type, schema_version, data)

    def _compute_matrix(self, class_labels, sample_weights=None):
        """Computes the matrix from prediction data"""
        y_pred_indexes = np.argmax(self._y_pred, axis=1)
        y_pred_labels = class_labels[y_pred_indexes]
        y_true = self._y

        if y_pred_labels.dtype.kind == 'f':
            class_labels = class_labels.astype(str)
            y_true = y_true.astype(str)
            y_pred_labels = y_pred_labels.astype(str)

        return sklearn.metrics.confusion_matrix(y_true=y_true,
                                                y_pred=y_pred_labels,
                                                sample_weight=sample_weights,
                                                labels=class_labels)

    def compute(self, sample_weights=None, class_labels=None):
        """Computes the score for the metric"""
        if class_labels is None:
            raise ValueError("Class labels required to compute \
                             ConfusionMatrixMetric")
        string_labels = [str(label) for label in class_labels]
        self._data[ConfusionMatrixMetric.CLASS_LABELS] = string_labels
        matrix = self._compute_matrix(class_labels,
                                      sample_weights=sample_weights)
        self._data[ConfusionMatrixMetric.MATRIX] = matrix
        ret = ConfusionMatrixMetric._data_to_dict(self._data)
        return Metric._make_json_safe(ret)

    @staticmethod
    def aggregate(scores):
        """Folds several scores from a computed metric together
        :param scores: a list of computed scores
        :return: the aggregated scores
        """
        if len(scores) == 0:
            raise ValueError("Scores must not be empty to aggregate")
        score_data = [score[Metric.DATA] for score in scores]
        matrices = [d[ConfusionMatrixMetric.MATRIX] for d in score_data]
        matrix_sum = np.sum(matrices, axis=0)
        agg_class_labels = score_data[0][ConfusionMatrixMetric.CLASS_LABELS]
        data_agg = {
            ConfusionMatrixMetric.CLASS_LABELS: agg_class_labels,
            ConfusionMatrixMetric.MATRIX: matrix_sum
        }
        ret = ConfusionMatrixMetric._data_to_dict(data_agg)
        return Metric._make_json_safe(ret)


class ResidualsMetric(RegressionMetric):
    """Residuals Metric"""

    SCHEMA_TYPE = constants.Metric.SCHEMA_TYPE_RESIDUALS
    SCHEMA_VERSION = 'v1'

    EDGES = 'bin_edges'
    COUNTS = 'bin_counts'

    @staticmethod
    def _data_to_dict(data):
        schema_type = ResidualsMetric.SCHEMA_TYPE
        schema_version = ResidualsMetric.SCHEMA_VERSION
        return Metric._data_to_dict(schema_type, schema_version, data)

    def compute(self, sample_weights=None, bin_info=None,
                y_min=None, y_max=None, y_std=None):
        if y_std is None:
            raise ValueError("y_std required to compute ResidualsMetric")

        num_bins = 10
        # If full dataset targets are all zero we still need a bin
        y_std = y_std if y_std != 0 else 1
        residuals = self._y_pred - self._y
        counts, edges = self._hist_by_bound(residuals, 2 * y_std, num_bins)
        ResidualsMetric._simplify_edges(residuals, edges)

        self._data[ResidualsMetric.EDGES] = edges
        self._data[ResidualsMetric.COUNTS] = counts
        ret = ResidualsMetric._data_to_dict(self._data)
        return Metric._make_json_safe(ret)

    def _hist_by_bound(self, values, bound, num_bins):
        bound = int(abs(bound))
        bin_size = bound / num_bins
        bin_edges = np.linspace(-bound, bound, num_bins)
        num_decimal_places = max(2, -1 * int(np.log10(bin_size)) + 2)
        for i, edge in enumerate(bin_edges):
            bin_edges[i] = np.around(edge, decimals=num_decimal_places)
        bins = np.r_[-np.inf, bin_edges, np.inf]
        return np.histogram(values, bins=bins)

    @staticmethod
    def _simplify_edges(residuals, edges):
        """Set the first and last edges of the histogram to be real numbers
            If the minimum residual is in the outlier bin then the left
            edge is set to that residual value. Otherwise, the left edge
            is set to be evenly spaced with the rest of the bins
            This is repeated on the right side of the histogram
        """
        assert(len(edges) >= 4)
        min_residual = np.min(residuals)

        # Keep left edge greater than negative infinity
        if min_residual < edges[1]:
            edges[0] = min_residual
        else:
            edges[0] = edges[1] - np.abs(edges[2] - edges[1])

        # Keep right edge less than infinity
        max_residual = np.max(residuals)
        if max_residual >= edges[-2]:
            edges[-1] = max_residual
        else:
            edges[-1] = edges[-2] + np.abs(edges[-2] - edges[-3])

    @staticmethod
    def aggregate(scores):
        """Folds several scores from a computed metric together
        :param scores: a list of computed scores
        :return: the aggregated scores
        """
        if len(scores) == 0:
            raise ValueError("Scores must not be empty to aggregate")
        score_data = [score[Metric.DATA] for score in scores]
        edges = [d[ResidualsMetric.EDGES] for d in score_data]
        counts = [d[ResidualsMetric.COUNTS] for d in score_data]
        agg_edges = ResidualsMetric._aggregate_edges(edges)
        agg_counts = np.sum(counts, axis=0)

        data_agg = {
            ResidualsMetric.EDGES: agg_edges,
            ResidualsMetric.COUNTS: agg_counts
        }
        ret = ResidualsMetric._data_to_dict(data_agg)
        return Metric._make_json_safe(ret)

    @staticmethod
    def _aggregate_edges(all_edges):
        all_edges_arr = np.array(all_edges)
        ret = np.copy(all_edges_arr[0])
        ret[0] = np.min(all_edges_arr[:, 0])
        ret[-1] = np.max(all_edges_arr[:, -1])
        return ret.tolist()


class PredictedTrueMetric(RegressionMetric):
    """Predicted vs True Metric"""

    SCHEMA_TYPE = constants.Metric.SCHEMA_TYPE_PREDICTIONS
    SCHEMA_VERSION = 'v1'

    AVERAGES = 'bin_averages'
    ERRORS = 'bin_errors'
    EDGES = 'bin_edges'
    COUNTS = 'bin_counts'

    @staticmethod
    def _data_to_dict(data):
        schema_type = PredictedTrueMetric.SCHEMA_TYPE
        schema_version = PredictedTrueMetric.SCHEMA_VERSION
        return Metric._data_to_dict(schema_type, schema_version, data)

    def compute(self, sample_weights=None, bin_info=None,
                y_min=None, y_max=None, y_std=None):
        if bin_info is None:
            raise ValueError("bin_info is required to \
                             compute PredictedTrueMetric")

        legacy_format = _predvstrue_compute(self._y, self._y_pred, bin_info)
        new_data = PredictedTrueMetric._legacy_format_to_data(legacy_format)
        self._data = new_data
        ret = PredictedTrueMetric._data_to_dict(self._data)
        return Metric._make_json_safe(ret)

    @staticmethod
    def _data_to_legacy_format(data):
        bin_averages = data[PredictedTrueMetric.AVERAGES]
        bin_errors = data[PredictedTrueMetric.ERRORS]
        bin_edges = data[PredictedTrueMetric.EDGES]
        bin_counts = data[PredictedTrueMetric.COUNTS]
        bin_starts = bin_edges[0:-1]
        bin_ends = bin_edges[1:]
        return {
            constants.Preds_Reg.TRUE_VALS_BINS_START: bin_starts,
            constants.Preds_Reg.TRUE_VALS_BINS_END: bin_ends,
            constants.Preds_Reg.AVG_PRED_VALS_PER_BIN: bin_averages,
            constants.Preds_Reg.PRED_ERROR_PER_BIN: bin_errors,
            constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN: bin_counts
        }

    @staticmethod
    def _legacy_format_to_data(d):
        bin_starts = d[constants.Preds_Reg.TRUE_VALS_BINS_START]
        bin_ends = d[constants.Preds_Reg.TRUE_VALS_BINS_END]
        bin_averages = d[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN]
        bin_errors = d[constants.Preds_Reg.PRED_ERROR_PER_BIN]
        bin_counts = d[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN]
        bin_edges = np.append(bin_starts, bin_ends[-1])

        data = {
            PredictedTrueMetric.AVERAGES: bin_averages,
            PredictedTrueMetric.ERRORS: bin_errors,
            PredictedTrueMetric.COUNTS: bin_counts,
            PredictedTrueMetric.EDGES: bin_edges,
        }
        return data

    @staticmethod
    def aggregate(scores):
        """Folds several scores from a computed metric together
        :param scores: a list of computed scores
        :return: the aggregated scores
        """
        if len(scores) == 0:
            raise ValueError("Scores must not be empty to aggregate")

        score_data = [score[Metric.DATA] for score in scores]
        to_legacy_dict = PredictedTrueMetric._data_to_legacy_format
        score_dicts = [to_legacy_dict(d) for d in score_data]
        dict_agg = _predvstrue_mean(score_dicts)
        data_agg = PredictedTrueMetric._legacy_format_to_data(dict_agg)
        ret = PredictedTrueMetric._data_to_dict(data_agg)
        return Metric._make_json_safe(ret)
