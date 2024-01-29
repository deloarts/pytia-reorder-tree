"""
    CATIA Reorder Graph Tree window handler.
    This module handles the graph tree window command.
"""

from time import sleep

from app.log import console
from app.log import log
from app.protocols.window_protocol import WindowProtocol
from app.window_handler import BaseWindow
from exceptions import WindowNotConnectedError
from pycatia.in_interfaces.application import Application
from pywinauto.controls.win32_controls import ButtonWrapper
from pywinauto.controls.win32_controls import ListBoxWrapper
from resources import resource


class ReorderWindow(BaseWindow, WindowProtocol):
    """ReorderWindow class. Handles the reorder graph tree window of the product."""

    def __init__(self, caa: Application) -> None:
        """Inits the class.

        Args:
            caa (Application): The catia application instance.
        """
        super().__init__(
            caa=caa,
            window_name=resource.applied_keywords.reorder_window_name,
        )

        self._btn_ok: ButtonWrapper | None = None
        self._btn_apply: ButtonWrapper | None = None
        self._btn_abort: ButtonWrapper | None = None
        self._btn_up: ButtonWrapper | None = None
        self._btn_down: ButtonWrapper | None = None
        self._list_box: ListBoxWrapper | None = None

    def connect(self) -> None:
        """Connects to the reorder graph tree window.

        Requires:
            The product tree nodes must be selected (CATIA.Document.Selection) before
            calling this method.

        Raises:
            WindowNotConnectedError: Raised then no connection to the window can be
            established.
        """
        try:
            self._caa.start_command(resource.applied_keywords.reorder_cmd_name)
            log.logger.info(
                f"Command {resource.applied_keywords.reorder_cmd_name!r} issued."
            )

            with console.status("Connecting to 'reorder graph tree' window..."):
                sleep(1)  # TODO: Make this not depending on sleep
                self._get_window()
                self._get_window_children()

            log.logger.info(
                f"Connected to {resource.applied_keywords.reorder_window_name!r} window."
            )
        except Exception as e:
            raise WindowNotConnectedError(
                f"Failed to connect to {resource.applied_keywords.reorder_window_name!r} "
                "window. This may be caused by an inactive window or a timeout in the "
                "connection.",
                with_trace=False,
            ) from e

    def _get_window_children(self) -> None:
        """Assigns the window elements to the appropriate properties."""
        assert self._window is not None
        for child in self._window.children():
            if child.window_text() == resource.applied_keywords.reorder_node_ok:
                self._btn_ok = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.reorder_node_apply:
                self._btn_apply = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.reorder_node_abort:
                self._btn_abort = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.reorder_node_move_up:
                self._btn_up = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.reorder_node_move_down:
                self._btn_down = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.reorder_node_list_box:
                self._list_box = ListBoxWrapper(child)
        assert all(
            [
                self._btn_ok,
                self._btn_apply,
                self._btn_abort,
                self._btn_up,
                self._btn_down,
                self._list_box,
            ]
        )

    @property
    def btn_ok(self) -> ButtonWrapper:
        assert self._btn_ok is not None
        return self._btn_ok

    @property
    def btn_apply(self) -> ButtonWrapper:
        assert self._btn_apply is not None
        return self._btn_apply

    @property
    def btn_abort(self) -> ButtonWrapper:
        assert self._btn_abort is not None
        return self._btn_abort

    @property
    def btn_up(self) -> ButtonWrapper:
        assert self._btn_up is not None
        return self._btn_up

    @property
    def btn_down(self) -> ButtonWrapper:
        assert self._btn_down is not None
        return self._btn_down

    @property
    def list_box(self) -> ListBoxWrapper:
        assert self._list_box is not None
        return self._list_box
