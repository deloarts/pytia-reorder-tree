"""
    Logging submodule.
    Exposes the global log and console variable.
"""

import logging

from const import LOG_FORMAT
from resources import resource
from rich.console import Console
from rich.logging import RichHandler


class Log:
    """Logging module class."""

    def __init__(self, debug: bool = True) -> None:
        """Inits the class

        Args:
            debug (bool, optional): Wether to display debug messages or not. \
                Defaults to True.
        """
        logging.basicConfig(
            level="NOTSET", format=LOG_FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )
        self._log = logging.getLogger("rich")
        self._log.setLevel(logging.DEBUG if debug else logging.INFO)
        self._log.debug("Logging module initialized.")

    @property
    def logger(self) -> logging.Logger:
        return self._log


log = Log(debug=resource.settings.debug)
console = Console()
