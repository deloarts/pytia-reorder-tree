"""
    Exit submodule. Handles smooth exists in the terminal.
"""

import sys
from time import sleep

from app.log import log


class Exit:
    """Exit class."""

    @staticmethod
    def close() -> None:
        """Terminates the app. Closes the terminal."""
        log.logger.info("Closing application.")
        sleep(2)
        sys.exit()

    @staticmethod
    def keep_open() -> None:
        """Terminates the app. Keeps the terminal open until the user presses enter."""
        log.logger.warning("Application terminated. Press ENTER to exit.")
        input()
        sys.exit()
