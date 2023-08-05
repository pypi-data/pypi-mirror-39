# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the data context classes."""
import logging
import os

from azureml import _async
from azureml.core import Datastore
from azureml.train.automl._cachestore import _MemoryCacheStore, _FileCacheStore, _AzureFileCacheStore
from .utilities import _get_ts_params_dict


class BaseDataContext(object):
    """
    Base data context class for input raw data and output transformed data.
    """

    def __init__(self, X, y=None,
                 X_valid=None,
                 y_valid=None,
                 sample_weight=None,
                 sample_weight_valid=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None,
                 num_cv_folds=None,
                 validation_size=None,
                 run_id=None,
                 enable_cache=True,
                 data_store=None,
                 **kwargs):
        """
        Constructor for the BaseDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        :param num_cv_folds: Number of cross validation folds
        :type num_cv_folds: integer
        :param validation_size: Percentage of data to be held out for validation
        :type validation_size: Double
        :param run_id: run id
        :type run_id: str
        :param data_store: data store
        :type data_store: azureml.core.AbstractAzureStorageDatastore
        """
        self.run_id = run_id
        self.X = X
        self.y = y
        self.X_valid = X_valid
        self.y_valid = y_valid
        self.sample_weight = sample_weight
        self.sample_weight_valid = sample_weight_valid
        self.x_raw_column_names = x_raw_column_names
        self.cv_splits_indices = cv_splits_indices
        self.num_cv_folds = num_cv_folds
        self.validation_size = validation_size
        self.enable_cache = enable_cache
        self.data_store = data_store


class RawDataContext(BaseDataContext):
    """
    Input raw data context
    """

    def __init__(self,
                 task_type,
                 X,  # DataFlow or DataFrame
                 y=None,  # DataFlow or DataFrame
                 X_valid=None,  # DataFlow
                 y_valid=None,  # DataFlow
                 sample_weight=None,
                 sample_weight_valid=None,
                 preprocess=None,
                 lag_length=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None,
                 num_cv_folds=None,
                 validation_size=None,
                 timeseries=False,
                 timeseries_param_dict=None,
                 automl_settings_obj=None,
                 run_id=None,
                 enable_cache=True,
                 data_store=None,
                 run_target='local',
                 **kwargs):
        """
        Constructor for the RawDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :param preprocess: The switch controls the preprocess.
            :type preprocess: bool
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        :param task_type: constants.Tasks.CLASSIFICATION or constants.Tasks.REGRESSION
        :type task_type: constants.Tasks
        :param num_cv_folds: Number of cross validation folds
        :type num_cv_folds: integer
        :param validation_size: Percentage of data to be held out for validation
        :type validation_size: Double
        :param automl_settings_obj: User settings specified when creating AutoMLConfig.
        :type automl_settings_obj: str or dict
        :param run_id: run id
        :type run_id: str
        :param data_store: data store
        :type data_store: azureml.core.AbstractAzureStorageDatastore
        :param run_target: run target
        :type run_target: str
        """
        self.preprocess = preprocess
        self.run_target = run_target
        self.lag_length = lag_length
        self.task_type = task_type
        self.timeseries = timeseries
        self.timeseries_param_dict = timeseries_param_dict

        if automl_settings_obj is not None:
            validation_size = automl_settings_obj.validation_size
            num_cv_folds = automl_settings_obj.n_cross_validations
            self.timeseries = automl_settings_obj.is_timeseries
            self.timeseries_param_dict = _get_ts_params_dict(automl_settings_obj)

        super().__init__(X=X, y=y,
                         X_valid=X_valid,
                         y_valid=y_valid,
                         sample_weight=sample_weight,
                         sample_weight_valid=sample_weight_valid,
                         x_raw_column_names=x_raw_column_names,
                         cv_splits_indices=cv_splits_indices,
                         num_cv_folds=num_cv_folds,
                         validation_size=validation_size,
                         run_id=run_id,
                         enable_cache=enable_cache,
                         data_store=data_store)


class TransformedDataContext(BaseDataContext):
    def __init__(self,
                 X,  # DataFrame
                 y=None,  # DataFrame
                 X_valid=None,  # DataFrame
                 y_valid=None,  # DataFrame
                 sample_weight=None,
                 sample_weight_valid=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None,
                 num_cv_folds=None,
                 validation_size=None,
                 run_targets='local',
                 run_id=None,
                 data_store=None,
                 enable_cache=True,
                 logger=logging.getLogger(__name__),
                 **kwargs):
        """
        Constructor for the TransformerDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        :param num_cv_folds: Number of cross validation folds
        :type num_cv_folds: integer
        :param validation_size: Fraction of data to be held out for validation
        :type validation_size: Float
        :param run_id: run id
        :type run_id: str
        :param data_store: data store
        :type data_store: azureml.core.AbstractAzureStorageDatastore
        :param logger: module logger
        :type logger: logger
        """
        super().__init__(X=X, y=y,
                         X_valid=X_valid,
                         y_valid=y_valid,
                         sample_weight=sample_weight,
                         sample_weight_valid=sample_weight_valid,
                         x_raw_column_names=x_raw_column_names,
                         cv_splits_indices=cv_splits_indices,
                         num_cv_folds=num_cv_folds,
                         validation_size=validation_size,
                         run_id=run_id,
                         enable_cache=enable_cache)
        self.run_targets = run_targets
        self.data_store = data_store
        self.module_logger = logger
        if self.module_logger is None:
            self.module_logger = logging.getLogger(__name__)
            self.module_logger.propagate = False

        self.cache_store = self._get_cache_store()
        self.transformers = dict()
        self._pickle_keys = ["X", "y", "X_valid", "y_valid", "sample_weight", "sample_weight_valid",
                             "x_raw_column_names", "cv_splits_indices", "run_id", "transformers",
                             "cv_splits"]
        self._num_workers = os.cpu_count()
        self.transformers = dict()
        self.cv_splits = None

    def _set_transformer(self, x_transformer=None, lag_transformer=None, y_transformer=None, ts_transformer=None):
        """
        Set the x_transformer and lag_transformer.

        :param x_transformer: transformer for x transformation.
        :param lag_transformer: lag transformer.
        :param y_transformer: transformer for y transformation.
        :param ts_transformer: transformer for timeseries data transformation.
        """
        self.transformers['x_transformer'] = x_transformer
        self.transformers['lag_transformer'] = lag_transformer
        self.transformers['y_transformer'] = y_transformer
        self.transformers['ts_transformer'] = ts_transformer

    def _get_engineered_feature_names(self):
        """
        Get the enigneered feature names available in different transformer.
        """
        if self.transformers['ts_transformer'] is not None:
            return self.transformers['ts_transformer'].get_engineered_feature_names()
        if self.transformers['lag_transformer'] is not None:
            return self.transformers['lag_transformer'].get_engineered_feature_names()
        elif self.transformers['x_transformer'] is not None:
            return self.transformers['x_transformer'].get_engineered_feature_names()
        else:
            return self.x_raw_column_names

    def _refit_transformers(self, X, y):
        """
        This function refits raw training data on the data and lagging transformers
        """
        if self.transformers['x_transformer'] is not None:
            self.transformers['x_transformer'].fit(X, y)

        if self.transformers['lag_transformer'] is not None:
            self.transformers['lag_transformer'].fit(X, y)

    def _load_from_cache(self):
        """
        loads data from cache store
        """
        self.cache_store.load()
        retrieve_data_list = self.cache_store.get(self._pickle_keys)

        super().__init__(X=retrieve_data_list.get('X'), y=retrieve_data_list.get('y'),
                         X_valid=retrieve_data_list.get('X_valid'),
                         y_valid=retrieve_data_list.get('y_valid'),
                         sample_weight=retrieve_data_list.get('sample_weight'),
                         sample_weight_valid=retrieve_data_list.get('sample_weight_valid'),
                         x_raw_column_names=retrieve_data_list.get('x_raw_column_names'),
                         cv_splits_indices=retrieve_data_list.get('cv_splits_indices'))
        self.transformers = retrieve_data_list.get('transformers')
        self.cv_splits = retrieve_data_list.get('cv_splits')

    def _update_cache(self):
        """
        updates cache based on run id
        """
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _async.TaskQueue(worker_pool=worker_pool,
                              _ident=__name__,
                              _parent_logger=self.module_logger) as tq:
            for k in self._pickle_keys:
                tasks.append(tq.add(self._add_to_cache, k))

        map(lambda task: task.wait(), tasks)
        worker_pool.shutdown()

    def _add_to_cache(self, k):
        self.cache_store.add([k], [self.__dict__.get(k)])

    def _get_cache_store(self):
        """
        gets cache store based on run type
        """
        try:
            if self.run_targets == "local" and self.run_id is not None and self.enable_cache:
                cache_store = _FileCacheStore(path=self.run_id, module_logger=self.module_logger)
                return cache_store

            if self.run_id is not None and self.data_store is not None and self.enable_cache:
                cache_store = _AzureFileCacheStore(path=self.run_id,
                                                   account_key=self.data_store.account_key,
                                                   account_name=self.data_store.account_name,
                                                   module_logger=self.module_logger)
                return cache_store
        except Exception as e:
            self.module_logger.warning("Failed to get store, fallback to memorystore {}, {}".format(self.run_id, e))

        cache_store = _MemoryCacheStore()

        return cache_store

    def _get_azure_file_cache_store(self):
        return _AzureFileCacheStore(path=self.run_id.lower(),
                                    account_key=self.data_store.account_key,
                                    account_name=self.data_store.account_name,
                                    module_logger=self.module_logger)

    def cleanup(self):
        """
        cache cleanup
        """
        self.cache_store.unload()
