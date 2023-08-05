# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for automl picklers."""

import _pickle as cPickle

from abc import ABC, abstractmethod

# This is the highest protocol number for 3.6.
DEFAULT_PICKLER_VERSION = 4


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
