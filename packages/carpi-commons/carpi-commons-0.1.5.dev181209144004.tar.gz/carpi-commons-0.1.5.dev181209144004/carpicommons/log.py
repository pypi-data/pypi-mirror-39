"""
CARPI COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from logging import Logger, getLogger, info, DEBUG, INFO
from logging.config import fileConfig, dictConfig
from os.path import isfile
from sys import exc_info
from traceback import format_exception

from carpicommons.errors import CarPiExitException

_LOGGER: Logger = None

DEFAULT_CONFIG = dict(
    version=1,
    formatters={
        'f': {
            'format': '[%(asctime)s.%(msecs)03d] [%(name)-15s] %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': DEBUG
        }
    },
    root={
        'handlers': ['h'],
        'level': INFO
    }
)


def configure_logging(config_files: list,
                      dict_config: dict=None):
    for config_file in config_files:
        if isfile(config_file):
            fileConfig(config_file)
            info("Logging configuration loaded: {}".format(config_file))
            return

    dictConfig(dict_config if dict_config else DEFAULT_CONFIG)
    info("Dictionary configuration loaded"
         if dict_config
         else "Default configuration loaded")


def init_logging(daemon_name: str):
    _LOGGER = getLogger(daemon_name)


def logger(name: str=None) -> Logger:
    return getLogger(name) if name else _LOGGER


def _print_exception(exc_type, exc, traceback):
    out: list = format_exception(exc_type, exc, traceback, limit=64)
    _LOGGER.critical('\n'.join(out))


def log_exception(ex: CarPiExitException):
    _LOGGER.critical("A known error has occurred that forced the daemon to shut down!")
    _LOGGER.critical("The error was:")
    _LOGGER.critical("[%s] %s", ex.exit_code, ex.exc_message)
    _LOGGER.critical("Stack Trace ahead:")
    log_unhandled_exception(False)


def log_unhandled_exception(log_prefix_message: bool=True):
    exc_type, exc, traceback = exc_info()
    if log_prefix_message:
        _LOGGER.critical("An unexpected error has forced the daemon to shut down!")
        _LOGGER.critical("Exception detail:")
    _print_exception(exc_type, exc, traceback)
    del exc_type, exc, traceback
