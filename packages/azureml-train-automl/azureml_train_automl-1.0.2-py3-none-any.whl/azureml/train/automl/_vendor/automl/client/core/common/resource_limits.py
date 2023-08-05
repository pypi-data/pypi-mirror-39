# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Implementation of resource limits with fallback for systems
which do not support the python resource module.
"""
import sys
import time
import warnings
from io import StringIO
from logging import getLogger
from sys import platform

if platform == "linux" or platform == "linux2":
    simple_platform = "linux"
elif platform == "darwin":
    simple_platform = "osx"
elif platform == "win32":
    simple_platform = "win"
else:
    simple_platform = "unknown"

TIME_CONSTRAINT = 'wall_time_in_s'

default_resource_limits = {
    # note that this is approximate
    'mem_in_mb': None,
    'cpu_time_in_s': None,
    # use 1 min for cluster runs.
    TIME_CONSTRAINT: 60 * 10,
    'num_processes': None,
    'grace_period_in_s': None,
    'logger': None
}


# use this for module functions
class safe_enforce_limits(object):
    """Method to allow for early termination of an execution."""
    try:
        import resource
        # see https://github.com/sfalkner/pynisher
        from automl.client.core.common import limit_function_call_spawn \
            as pynisher
        ok = True
    except ImportError as e:
        # this is the error we're expecting
        assert str(e) == "No module named 'resource'"
        ok = False

    def get_param_str(self, kwargs):
        """
        :param kwargs:
        :return:
        """
        s = ""
        for k, v in kwargs.items():
            s += k + "=" + str(v) + ", "
        return s

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        self.log = getLogger(__name__)
        self.log.info("limits set to %s" % self.get_param_str(kwargs))

        if kwargs.get('logger', None) is not None:
            self.log.warning("logger specified for pynisher.")
        else:
            kwargs['logger'] = self.log
        if not self.ok:
            # TODO Add the windows resource limit in core sdk
            # change the code to use the libray's resource enforcement.
            if simple_platform != "win":
                self.log.warning("Unable to enforce resource limits.")
                warnings.warn("Unable to enforce resource limits.")
        self.obj = None
        if self.ok:
            self.obj = self.pynisher.enforce_limits(*args, **kwargs)

        self.exit_status = None
        self.wall_clock_time = None
        self.result = None

    def __call__(self, func):
        """
        :param func:
        :return:
        """
        if self.ok:
            def func2(*args, **kwargs):

                # capture and log stdout, stderr
                # out, err = sys.stdout, sys.stderr
                # out_str, err_str = StringIO(), StringIO()
                # sys.stdout, sys.stderr = out_str, err_str

                f_obj = self.obj.__call__(func)
                r = f_obj(*args, **kwargs)
                self.exit_status = f_obj.exit_status
                self.wall_clock_time = f_obj.wall_clock_time
                self.result = f_obj.result

                # out_str, err_str = out_str.getvalue(), err_str.getvalue()
                # if err_str != "": self.log.error(err_str)
                # if out_str != "": self.log.info(out_str)
                # sys.stdout, sys.stderr = out, err
                return r
            return func2
        return func
