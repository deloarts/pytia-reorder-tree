"""
    Window handler submodule.
    This module holds the base class for all window classes.
"""

from pycatia.in_interfaces.application import Application
from pywinauto import Desktop


class BaseWindow:
    """Base window class for this submodule."""

    def __init__(self, caa: Application, window_name: str) -> None:
        """Inits the class.

        Args:
            caa (Application): The catia application instance.
            window_name (str): The name of the window to which the connection must be \
                established.
        """
        self._caa = caa
        self._window = None
        self._window_name = window_name

    def _get_window(self) -> None:
        """
        Gets the window by name from all open windows.
        Window name ist setup at instantiation.
        """
        windows = Desktop().windows()
        self._window = None
        for window in windows:
            if self._window_name in window.window_text():
                window.set_focus()
                self._window = window
        assert self._window is not None
