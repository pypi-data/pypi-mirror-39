# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Classes for automl cache store."""
import logging
import os
import sys  # noqa F401 # dynamically evaluated to get caller
import tempfile
import uuid

from abc import ABC, abstractmethod

from azureml import _async
from azureml._vendor.azure_storage.file import FileService, models, ContentSettings
from azureml.telemetry.activity import log_activity
from azureml.train.automl._automlpickler import _DefaultPickler


class _CacheStore(ABC):
    """
    ABC for cache store
    """

    def __init__(self, path=None, max_retries=3, module_logger=logging.getLogger()):
        """
        Cache store constructor
        :param path: path of the store
        :param max_retries: max retries to get/put from/to store
        :param module_logger: logger
        """
        self.path = path
        self.cache_items = dict()
        self.max_retries = max_retries
        self.module_logger = module_logger

    @abstractmethod
    def load(self):
        """
        load - abstract method
        """
        pass

    @abstractmethod
    def unload(self):
        """
        unload - abstract method
        """
        pass

    def add(self, keys, values):
        """
        adds to store
        :param keys: store key
        :param values: store value
        """
        for k, v in zip(keys, values):
            self.cache_items[k] = v

    def add_or_get(self, key, value):
        """
        add or get from store
        :param key: store key
        :param value: store value
        :return: value
        """
        val = self.cache_items.get(key, None)
        if val is not None:
            return val

        self.add([key], [value])
        return value

    def get(self, keys, default=None):
        """
        gets value from store
        :param default: default value
        :param keys: store keys
        :return: values
        """
        vals = dict()
        for k in keys:
            vals[k] = self.cache_items.get(k, default)

        return vals

    def set(self, key, value):
        """
        sets value to store
        :param key: store key
        :param value: store value
        """
        self.add([key], [value])

    def remove(self, key):
        """
        removes from store
        :param key: store key
        """
        obj = self.cache_items.pop(key)
        del obj

    def remove_all(self):
        """
        removes all entry from store
        """
        for k, v in self.cache_items.items():
            del v

        self.cache_items.clear()

    def __iter__(self):
        """
        store iterator
        :return:
        """
        return iter(self.cache_items.items())

    @staticmethod
    def _function_with_retry(fn, max_retries, logger, *args, **kwargs):
        """
        calling function with retry capability
        :param fn: function to be executed
        :param max_retries: number of retries
        :param logger: logger
        :param args: args
        :param kwargs: kwargs
        :return: Exception if failure, otherwise returns value from function call
        """
        retry_count = 0
        ex = None
        while retry_count < max_retries:
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                logger.warning("Execution failed {}".format(e))
                ex = e
            finally:
                retry_count += 1

        raise ex


class _MemoryCacheStore(_CacheStore):
    """
    MemoryCacheStore - stores value in memory
    """

    def __init__(self, path=None):
        """
        MemoryCacheStore - constructor
        """
        super(_MemoryCacheStore, self).__init__(path=path)

    def load(self):
        """
        loads from memory - NoOp
        """
        pass

    def unload(self):
        """
        unloads from memory
        """
        self.cache_items.clear()


class _AzureFileCacheStore(_CacheStore):
    """
    Cache store based on azure file system
    """

    def __init__(self, path,
                 account_name=None,
                 account_key=None,
                 pickler=_DefaultPickler(),
                 module_logger=logging.getLogger(__name__)
                 ):
        """
        AzureFileCacheStore - cache based on azure file system
        :param path: path of the store
        :param account_name: account name
        :param account_key: account key
        :param pickler: pickler, default is cPickler
        :param module_logger: logger
        """
        super(_AzureFileCacheStore, self).__init__()
        self.file_service = FileService(account_name=account_name,
                                        account_key=account_key)
        self.path = path.lower().replace('_', '-')
        self.file_service.create_share(self.path)
        self.pickler = pickler
        self.account_name = account_name
        self.account_key = account_key
        self.cache_items = dict()
        self._num_workers = os.cpu_count()
        self.module_logger = module_logger
        self.temp_location = _create_temp_dir()
        self.activity_prefix = "_AzureFileCacheStore"

    def add(self, keys, values):
        """
        adds to azure file store
        :param keys: keys
        :param values: values
        """
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _log_activity(logger=self.module_logger):
            with _async.TaskQueue(worker_pool=worker_pool, _ident=__name__,
                                  _parent_logger=self.module_logger) as tq:
                for k, v in zip(keys, values):
                    tasks.append(tq.add(self._function_with_retry,
                                        self._upload,
                                        self.max_retries,
                                        self.module_logger,
                                        k,
                                        v))

            map(lambda task: task.wait(), tasks)
            worker_pool.shutdown()

    def add_or_get(self, key, value):
        """
        add or gets from azure file store
        :param key:
        :param value:
        :return: unpickled value
        """
        val = self.cache_items.get(key, None)
        if val is None:
            self.add([key], [value])
            return {key: value}

        return self.get([key], None)

    def get(self, keys, default=None):
        """
        gets from azure file store & unpickles
        :param default: default value
        :param keys: store key
        :return: unpickled object
        """
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _log_activity(logger=self.module_logger):
            with _async.TaskQueue(worker_pool=worker_pool, _ident=__name__,
                                  _parent_logger=self.module_logger) as tq:
                for key in keys:
                    tasks.append(tq.add(self._function_with_retry,
                                        self._download_file,
                                        self.max_retries,
                                        self.module_logger,
                                        key))

            results = map(lambda task: task.wait(), tasks)
            worker_pool.shutdown()
            ret = dict()
            pickle_exception = None
            for result in results:
                try:
                    for key, val in result.items():
                        obj = default
                        if val is not None:
                            try:
                                obj = self.pickler.load(val)
                                self.cache_items[key] = key
                            finally:
                                self._try_remove_temp_file(path=val)
                        ret[key] = obj
                except Exception as e:
                    self.module_logger.warning("Pickle error {}".format(e))
                    pickle_exception = e

            if pickle_exception is not None:
                raise CacheException("Cache failure {}".format(pickle_exception))

        return ret

    def set(self, key, value):
        """
        sets values to store
        :param key: key
        :param value: value
        """
        self.add(key, value)

    def remove(self, key):
        """
        removes from store
        :param key: store key
        """
        with _log_activity(logger=self.module_logger):
            self._remove(self.path, [key])

    def remove_all(self):
        """
        removes all the file from cache
        """
        with _log_activity(logger=self.module_logger):
            self._remove(self.path, self.cache_items.keys())

    def load(self):
        """
        loads from azure file store
        """
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _log_activity(logger=self.module_logger):
            with _async.TaskQueue(worker_pool=worker_pool, _ident=__name__,
                                  _parent_logger=self.module_logger) as tq:
                tasks.append(tq.add(self._function_with_retry,
                                    self._get_azure_file_lists,
                                    self.max_retries,
                                    self.module_logger,
                                    self.path))

            map(lambda task: task.wait(), tasks)
            worker_pool.shutdown()

    def unload(self):
        """
        unloads the cache.
        """
        try:
            self.file_service.delete_share(share_name=self.path)
        except Exception as e:
            self.module_logger.warning("Failed to delete share {}, {}".format(self.path, e))

        self.cache_items.clear()
        _try_remove_dir(self.temp_location)

    def _remove(self, path, files):
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []

        with _async.TaskQueue(worker_pool=worker_pool, _ident=__name__,
                              _parent_logger=self.module_logger) as tq:
            for file in files:
                tasks.append(tq.add(self._function_with_retry,
                                    self._remove_from_azrue_file_store,
                                    self.max_retries,
                                    self.module_logger,
                                    path,
                                    file))

        map(lambda task: task.wait(), tasks)
        worker_pool.shutdown()

    def _remove_from_azrue_file_store(self, path, key):
        self.file_service.delete_file(path, directory_name=None, file_name=key)
        self.cache_items.pop(key)

    def _get_azure_file_lists(self, path):
        """
        gets list of files available from azure file store. similar to dir
        :param path: path
        """
        for dir_or_file in self.file_service.list_directories_and_files(share_name=path):
            if isinstance(dir_or_file, models.File):
                self.cache_items[dir_or_file.name] = dir_or_file.name

    def _download_file(self, file):
        """
        downloads from azure file store
        :param file:
        """
        temp_path = os.path.join(self.temp_location, file)
        try:
            self.file_service.get_file_to_path(share_name=self.path,
                                               directory_name=None,
                                               file_name=file,
                                               file_path=temp_path)
            self.cache_items[file] = temp_path
        except Exception:
            # get_file_to_path created temp file if file doesnt exists
            self._try_remove_temp_file(temp_path)
            raise

        return {file: temp_path}

    def _upload(self, file, obj):
        temp_path = os.path.join(self.temp_location, file)
        try:
            self.pickler.dump(obj, temp_path)
            self.file_service.create_file_from_path(share_name=self.path,
                                                    file_name=file,
                                                    directory_name=None,
                                                    content_settings=ContentSettings('application/x-binary'),
                                                    local_file_path=temp_path)
            self.cache_items[file] = file
        finally:
            self._try_remove_temp_file(temp_path)

    def _try_remove_temp_file(self, path):
        try:
            os.remove(path)
        except OSError as e:
            self.module_logger.warning("failed to remove temp file {}".format(e))

    def __del__(self):
        _try_remove_dir(self.temp_location)


class _FileCacheStore(_CacheStore):
    """
    FileCacheStore - cache store based on file system
    """

    def __init__(self, path, pickler=_DefaultPickler(), module_logger=None):
        """
        FileCacheStore - constructor
        :param module_logger:
        :param path: store path
        :param pickler: pickler, defaults to cPickler
        """
        super(_FileCacheStore, self).__init__()
        self.pickler = pickler
        self.module_logger = module_logger
        self._num_workers = os.cpu_count()
        self.path = _create_temp_dir()

    def add(self, keys, values):
        """
        pickles the object and adds to cache
        :param keys: store keys
        :param values: store values
        """
        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _log_activity(logger=self.module_logger):
            with _async.TaskQueue(worker_pool=worker_pool,
                                  _ident=__name__,
                                  _parent_logger=self.module_logger) as tq:
                for k, v in zip(keys, values):
                    tasks.append(tq.add(self._upload, k, v))

            map(lambda task: task.wait(), tasks)
            worker_pool.shutdown()

    def add_or_get(self, key, value):
        """
        adds or gets from the store
        :param key: store key
        :param value: store value
        :return: UnPickled object
        """
        val = self.cache_items.get(key, None)
        if val is not None:
            return self.get([key])

        self.add([key], [value])
        return value

    def get(self, keys, default=None):
        """
        gets unpickled object from store
        :param keys: store keys
        :param default: returns default value if not present
        :return: unpickled objects
        """
        res = dict()

        with _log_activity(logger=self.module_logger):
            for key in keys:
                path = self.cache_items.get(key, None)
                obj = default
                if path is not None:
                    obj = self.pickler.load(path)
                res[key] = obj

        return res

    def set(self, key, value):
        """
        sets to store
        :param key: store key
        :param value: store value
        """
        self.add([key], [value])

    def remove(self, key):
        """
        removes from store
        :param key: store key
        """
        with _log_activity(logger=self.module_logger):
            try:
                path = os.path.join(self.path, key)
                os.remove(path)
                self.cache_items.pop(key)
            except Exception as e:
                self.module_logger.warning("remove from store failed {}".format(e))

    def remove_all(self):
        """
        removes all the cache from store
        """
        length = self.cache_items.__len__()

        worker_pool = _async.WorkerPool(max_workers=self._num_workers)
        tasks = []
        with _log_activity(logger=self.module_logger):
            with _async.TaskQueue(worker_pool=worker_pool,
                                  _ident=__name__,
                                  _parent_logger=self.module_logger) as tq:
                while length > 0:
                    length -= 1
                    k, v = self.cache_items.popitem()
                    tasks.append(tq.add(self._delete_file, k))

            map(lambda task: task.wait(), tasks)
            worker_pool.shutdown()

    def load(self):
        """
        loads from store
        """
        with _log_activity(logger=self.module_logger):
            for f in os.listdir(self.path):
                path = os.path.join(self.path, f)
                self.cache_items[f] = path

    def unload(self):
        """
        unloads from store
        """
        self.remove_all()
        _try_remove_dir(self.path)

    def _upload(self, key, obj):
        try:
            path = os.path.join(self.path, key)
            self.pickler.dump(obj, path=path)
            self.cache_items[key] = path
        except Exception as e:
            self.module_logger.error("Uploading {} failed with {}".format(key, e))
            raise

    def _delete_file(self, k):
        try:
            path = os.path.join(self.path, k)
            os.remove(path)
        except Exception as e:
            self.module_logger.warning("remove from store failed {}".format(e))


def _create_temp_dir():
    """
    creates temp dir
    :return: temp location
    """
    try:
        return tempfile.mkdtemp()
    except OSError as e:
        raise CacheException("Failed to create temp folder {}. You can disable the "
                             "cache if space is concern. Setting to disable cache enable_cache=False".format(e))


def _try_remove_dir(path):
    """
    removes directory
    :param path: path to be removed
    """
    try:
        os.rmdir(path)
    except OSError:
        return False

    return True


def _log_activity(logger, custom_dimensions=None):
    """
    log activity collects the execution latency
    :param logger: logger
    :param custom_dimensions: custom telemetry dimensions
    :return: log activity
    """
    get_frame_expr = 'sys._getframe({}).f_code.co_name'
    caller = eval(get_frame_expr.format(2))
    telemetry_values = dict()
    telemetry_values['caller'] = caller

    if custom_dimensions is not None:
        telemetry_values.update(custom_dimensions)

    return log_activity(logger=logger, activity_name=caller, custom_dimensions=telemetry_values)


class CacheException(Exception):
    def __init__(self, *args, **kwargs):
        super(CacheException, self).__init__(*args, **kwargs)
