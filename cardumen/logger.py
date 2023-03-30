"""
Module for logging.
"""
import sys
from datetime import datetime
from enum import Enum

from cardumen.design_patterns import singleton


class LogLevel(Enum):
    """
    Enum for log levels.
    """
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

    def __le__(self, other):
        return self.value <= other.value


@singleton
class _Logger:
    """
    Class for logging.
    """

    def __init__(self):
        self._log_level = LogLevel.INFO
        self._log_file = None

    def _log(self, level: LogLevel, message: str):
        """
        Log message to file.
        """
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} [{level.name}] {message}"

        print(message, end='\n', file=sys.stdout)
        if self._log_file is not None:
            with open(self._log_file, 'a') as f:
                f.write(message + '\n')

    def debug(self, message: str):
        if self._log_level <= LogLevel.DEBUG:
            self._log(LogLevel.DEBUG, message)

    def info(self, message: str):
        if self._log_level <= LogLevel.INFO:
            self._log(LogLevel.INFO, message)

    def warning(self, message: str):
        if self._log_level <= LogLevel.WARNING:
            self._log(LogLevel.WARNING, message)

    def error(self, message: str):
        if self._log_level <= LogLevel.ERROR:
            self._log(LogLevel.ERROR, message)

    def critical(self, message: str):
        if self._log_level <= LogLevel.CRITICAL:
            self._log(LogLevel.CRITICAL, message)


def set_log_level(log_level: LogLevel):
    _Logger()._log_level = log_level


def set_log_file(log_file: LogLevel):
    _Logger()._log_file = log_file


log = _Logger()
