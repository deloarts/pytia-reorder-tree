"""
    Window-Protocols submodule.
"""

from typing import Any, Protocol

from pycatia.in_interfaces.application import Application


class WindowProtocol(Protocol):
    def connect(self) -> None:
        self._caa: Application
        self._window: Any
        self._window_name: str

    def _get_window(self) -> None:
        ...

    def _get_window_children(self) -> None:
        ...
