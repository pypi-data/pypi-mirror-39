# -*- coding: future_fstrings -*-

# Copyright 2018 Streamlit Inc. All rights reserved.

"""Logging module."""

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

import inspect
import logging
import sys

# Loggers for each name are saved here.
LOGGERS = dict()

# The global log level is set here across all names.
LOG_LEVEL = logging.DEBUG

# This boolean is True iff this is the proxy.
THIS_IS_PROXY = False


def set_log_level(level):
    """Set log level."""
    logger = get_logger(__name__)

    if isinstance(level, str):
        level = level.upper()
    if level == 'CRITICAL' or level == logging.CRITICAL:
        log_level = logging.CRITICAL
    elif level == 'ERROR' or level == logging.ERROR:
        log_level = logging.ERROR
    elif level == 'WARNING' or level == logging.WARNING:
        log_level = logging.WARNING
    elif level == 'INFO' or level == logging.INFO:
        log_level = logging.INFO
    elif level == 'DEBUG' or level == logging.DEBUG:
        log_level = logging.DEBUG
    else:
        msg = 'undefined log level "{}"'.format(level)
        logger.critical(msg)
        sys.exit(1)

    for log in LOGGERS.values():
        log.setLevel(log_level)

    global LOG_LEVEL
    LOG_LEVEL = log_level


def set_this_is_proxy():
    """Set the module-level global boolean THIS_IS_PROXY."""
    global THIS_IS_PROXY
    THIS_IS_PROXY = True
    for log in LOGGERS.values():
        setup_formatter(log)


def setup_formatter(logger):
    """Set up the console formatter for a given logger."""
    # Deregister any previous console loggers.
    if hasattr(logger, 'streamlit_console_handler'):
        logger.removeHandler(logger.streamlit_console_handler)

    # Creates the console handler for this logger.
    global THIS_IS_PROXY
    if THIS_IS_PROXY:
        formatter = logging.Formatter('- PROXY  %(levelname)-5s %(name)-20s: %(message)s')
    else:
        formatter = logging.Formatter('- CLIENT %(levelname)-5s %(name)-20s: %(message)s')
    logger.streamlit_console_handler = logging.StreamHandler()
    logger.streamlit_console_handler.setFormatter(formatter)

    # Register the new console logger.
    logger.addHandler(logger.streamlit_console_handler)


def init_aiohttp_logs():
    """Initialize aiohttp logs."""
    global LOGGER

    # https://docs.aiohttp.org/en/stable/logging.html
    logs = ['access', 'client', 'internal', 'server', 'web', 'websocket']
    for log in logs:
        name = 'aiohttp.{}'.format(log)
        get_logger(name)

    logger = get_logger(__name__)
    logger.debug('Initialized aiohttp logs')


def init_tornado_logs():
    """Initialize tornado logs."""
    global LOGGER

    # http://www.tornadoweb.org/en/stable/log.html
    logs = ['access', 'application', 'general']
    for log in logs:
        name = 'tornado.{}'.format(log)
        get_logger(name)

    logger = get_logger(__name__)
    logger.debug('Initialized tornado logs')


def get_logger(name):
    """Return a logger.

    Parameters
    ----------
    name : str
        The name of the logger to use. You should just pass in __name__.

    Returns
    -------
    Logger

    """
    global LOG_LEVEL

    if name in LOGGERS.keys():
        return LOGGERS[name]

    if name == 'root':
        log = logging.getLogger()
    else:
        log = logging.getLogger(name)

    log.setLevel(LOG_LEVEL)
    log.propagate = False
    setup_formatter(log)

    LOGGERS[name] = log

    return log
