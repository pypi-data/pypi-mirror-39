# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for automl picklers."""

import _pickle as cPickle
import os
import time

from abc import ABC, abstractmethod
from io import BytesIO

# This is the highest protocol number for 3.6.
DEFAULT_PICKLER_VERSION = 4

# Chunk meta file extension
CHUNK_META_FILE_EXTN = '.partition'

# No of retries
DEFAULT_NO_OF_RETRIES = 3


class _Pickler(ABC):
    """
    Pickler abstract class
    """
    def __init__(self):
        """
        Default pickler constructor
        """
        pass

    @abstractmethod
    def dump(self, obj, path, protocol=None):
        """
        dumps the object to file based on protocol
        :param obj: object to pickle
        :param path: pickler path
        :param protocol: pickler protocol version
        :return: path of pickler
        """
        pass

    @abstractmethod
    def load(self, path):
        """
        loads the object from path
        :param path: path for load
        """
        pass

    @abstractmethod
    def get_pickle_files(self, path):
        """
        gets file names of the given pickle file with path.
        :param path: path of pickle file
        :return: chunk files
        """
        pass

    def get_meta_file(self, path):
        """
        gets the meta file if available
        :param path: path of pickle file path
        :return: meta file path
        """
        return path

    def is_meta_file(self, path):
        """
        checks is meta file, default is true, chunking, etc.. overrides
        :param path: path of the pickle file
        :return: True
        """
        return True

    def get_name_without_extn(self, path):
        """
        gets the key without extension
        :param path: path of the file
        :return: key without extension
        """
        return os.path.splitext(path)[0]


class _DefaultPickler(_Pickler):
    """
    Default pickler based on python cPickler
    """
    def __init__(self):
        """
        Default pickler constructor
        """
        super(_DefaultPickler, self).__init__()

    def dump(self, obj, path, protocol=DEFAULT_PICKLER_VERSION):
        """
        dumps the object to file based on protocol
        :param obj: object to pickle
        :param path: pickler path
        :param protocol: pickler protocol version
        :return: path of pickler
        """
        try:
            with open(path, "wb") as f:
                cPickle.dump(obj, f)
        except Exception as e:
            raise Exception("Pickle error {}".format(e))

        return path

    def load(self, path):
        """
        unpickles the file
        :param path: pickler file path
        :return: UnPickled object
        """
        try:
            with open(path, "rb") as f:
                return cPickle.load(f)
        except Exception as e:
            raise Exception("UnPickle error {}".format(e))

    def get_pickle_files(self, path):
        """
        gets the pickle files. default behavir return passed path
        :param path: path of pickle file
        :return: path of pickle file
        """
        return [path]


class _ChunkPickler(_Pickler):
    """
    Chunk pickler based on python cPickler
    """
    def __init__(self, chunk_size=100000000, retries=DEFAULT_NO_OF_RETRIES):
        """
        Chunk pickler constructor
        :param chunk_size: chunk size
        :param retries: retries
        """
        self.chunk_size = chunk_size
        self._retries = retries
        super(_ChunkPickler, self).__init__()

    def dump(self, obj, path, protocol=DEFAULT_PICKLER_VERSION):
        """
        dumps the object to file based on protocol
        :param obj: object to pickle
        :param path: pickler path
        :param protocol: pickler protocol version
        :return: path of pickler
        """
        try:
            base_dir = os.path.dirname(path)
            pickle_file = os.path.basename(path)
            meta_file_name = self.get_meta_file(path)

            with BytesIO() as bio:
                cPickle.dump(obj, bio)
                bio.seek(0)
                chunk_content = bio.read(self.chunk_size)
                with self._try_open_file(meta_file_name, 'wt') as mf:
                    self._try_write_chunks(base_dir, bio, chunk_content, mf, pickle_file)
        except Exception as e:
            raise AutoMLPickleException("Pickle error {}".format(e))

        return path

    def _try_open_file(self, file_name, mode):
        exception_thrown = None
        for i in range(0, self._retries):
            try:
                return open(file_name, mode)
            except Exception as e:
                exception_thrown = e
                time.sleep(1)

        if exception_thrown:
            raise exception_thrown

    def _try_write_chunks(self, base_dir, bio, chunk_content, meta_file, pickle_file_name):
        """
        writes chunk into file and updates the meta data file
        :param base_dir: base directory
        :param bio: bite io
        :param chunk_content: chunk content
        :param meta_file: meta file
        :param pickle_file_name: pickle file name
        :return:
        """
        exception_thrown = None
        p = 0
        while len(chunk_content) > 0:
            file = os.path.join(base_dir, "{}.{}".format(pickle_file_name, str(p)))
            for i in range(0, self._retries):
                try:
                    with open(file, 'wb') as uc:
                        uc.write(chunk_content)
                    break
                except Exception as e:
                    exception_thrown = e
                    time.sleep(1)

            if exception_thrown:
                raise exception_thrown

            chunk_content = bio.read(self.chunk_size)
            p += 1
            meta_file.write(file)
            meta_file.write('\n')

    def load(self, path):
        """
        unpickles the file
        :param path: pickler file path
        :return: UnPickled object
        """
        exception_thrown = None

        try:
            chunk_files = self._get_chunk_files(path)

            with BytesIO() as content:
                for chunk_file in chunk_files:
                    for i in range(0, self._retries):
                        try:
                            with open(chunk_file, 'rb') as uc:
                                uc_content = uc.read()
                            break
                        except Exception as e:
                            exception_thrown = e
                            time.sleep(1)
                    if exception_thrown:
                        raise exception_thrown
                    content.write(uc_content)
                content.seek(0)
                return cPickle.load(content)
        except Exception as e:
            raise AutoMLPickleException("UnPickle error {}".format(e))

    def get_pickle_files(self, path):
        """
        gets the pickle files with meta file
        :param path: path of pickle file
        :return: pickle files with meta file
        """
        meta_file = self.get_meta_file(path)
        chunked_files = self._get_chunk_files(path)
        chunked_files.append(meta_file)
        return chunked_files

    def get_meta_file(self, path):
        """
        gets the meta file from path
        :param path: path of pickle file
        :return: pickle meta file name
        """
        base_dir = os.path.dirname(path)
        pickle_file = os.path.basename(path)
        return os.path.join(base_dir, "{}{}".format(pickle_file, CHUNK_META_FILE_EXTN))

    def is_meta_file(self, path):
        """
        Checks the file is meta file based on extension
        :param path: path of pickle file
        :return: True if meta file otherwise False
        """
        return path.endswith(CHUNK_META_FILE_EXTN)

    def _get_chunk_files(self, path):
        chunked_files = []
        meta_file = self.get_meta_file(path)
        exception_thrown = None

        for i in range(0, self._retries):
            try:
                with open(meta_file, 'r') as mf:
                    file = mf.readline()
                    file = file.replace('\n', '')
                    while len(file) > 0:
                        chunked_files.append(file)
                        file = mf.readline()
                        file = file.replace('\n', '')

                return chunked_files
            except Exception as e:
                exception_thrown = e
                time.sleep(1)

        if exception_thrown:
            raise AutoMLPickleException("Failed to get chunk files {}".format(exception_thrown))


class _NoOpPickler(_Pickler):
    """
    No operation pickler for memory based
    """
    def __init__(self):
        """
        Constructor
        """
        super(_NoOpPickler, self).__init__()
        pass

    def dump(self, obj, path, protocol=None):
        """
        no op
        :param obj: object to be dumped
        :param path: path
        :param protocol: protocol
        """
        pass

    def load(self, path):
        """
        load - No op
        :param path: path
        :return: path
        """
        return path

    def get_pickle_files(self, path):
        """
        gets the pickle files based on chunking
        :param path:
        :return:
        """
        return [path]


class AutoMLPickleException(Exception):
    """
    A class for automl pickle exception
    """
    def __init__(self, *args, **kwargs):
        super(AutoMLPickleException, self).__init__(*args, **kwargs)
