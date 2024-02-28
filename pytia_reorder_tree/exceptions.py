"""
    Module that holds all custom pytia exceptions.
"""

import sys
import traceback

from pytia.log import log


class BaseError(Exception):
    """Base class for all exceptions. Logs exceptions as error messages"""

    def __init__(self, msg: str, with_trace: bool = True) -> None:
        super().__init__(msg)
        if with_trace and traceback.extract_tb(sys.exc_info()[2]):
            log.exception(msg)
        else:
            log.error(msg)


class WindowNotConnectedError(BaseError):
    """Exception for pywinauto window connection error."""


class WarningError(BaseError):
    """Exception for warnings only."""
