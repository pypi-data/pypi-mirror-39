import logging
import traceback


def _get_null_logger(name='null_logger'):
    null_logger = logging.getLogger(name)
    null_logger.addHandler(logging.NullHandler())
    null_logger.propagate = False
    return null_logger


NULL_LOGGER = _get_null_logger()


def log_traceback(exception, logger):
    if logger is None:
        logger = NULL_LOGGER

    logger.error(exception)
    logger.error(traceback.format_exc())
