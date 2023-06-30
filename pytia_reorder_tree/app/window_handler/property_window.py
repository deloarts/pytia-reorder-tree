"""
    CATIA Properties window handler.
    This module handles the properties window of product tree nodes.
"""

from time import sleep

from app.log import console, log
from app.protocols.window_protocol import WindowProtocol
from app.window_handler import BaseWindow
from exceptions import WindowNotConnectedError
from pycatia.in_interfaces.application import Application
from pywinauto.controls.common_controls import TabControlWrapper
from pywinauto.controls.win32_controls import ButtonWrapper
from resources import resource


class PropertyWindow(BaseWindow, WindowProtocol):
    """PropertyWindow class. Handles the properties window of product tree nodes."""

    def __init__(self, caa: Application) -> None:
        """Inits the class.

        Args:
            caa (Application): The catia application instance.
        """
        super().__init__(
            caa=caa,
            window_name=resource.applied_keywords.props_window_name,
        )

        self._product_tab_visible: bool = False

        self._tab_product: TabControlWrapper | None = None
        self._btn_ok: ButtonWrapper | None = None
        self._btn_apply: ButtonWrapper | None = None
        self._btn_close: ButtonWrapper | None = None
        self._chk_bom: ButtonWrapper | None = None

    def connect(self) -> None:
        """Connects to the properties window.

        Requires:
            The product tree nodes must be selected (CATIA.Document.Selection) before
            calling this method.

        Raises:
            WindowNotConnectedError: Raised then no connection to the window can be
            established.
        """
        try:
            self._caa.start_command(resource.applied_keywords.props_cmd_name)
            log.logger.info(
                f"Command {resource.applied_keywords.props_cmd_name!r} issued."
            )

            with console.status("Connecting to 'properties' window..."):
                sleep(1)  # TODO: Make this not depending on sleep
                self._get_window()
                self._get_window_children()

            log.logger.info(
                f"Connected to {resource.applied_keywords.props_window_name!r} window."
            )

        except Exception as e:
            raise WindowNotConnectedError(
                f"Failed to connect to {resource.applied_keywords.props_window_name!r} "
                "window. This may be caused by an inactive window or a timeout in the "
                "connection.",
                with_trace=True if resource.settings.debug else False,
            ) from e

    def uncheck_bom(self) -> None:
        """Sets the value of the 'Visualize in the bill of material' checkbox to 0.

        Requires:
            Method `connect` must be called first.
        """

        if (
            self._product_tab_visible
            and self._chk_bom is not None
            and self._tab_product is not None
            and self._tab_product.is_visible()
        ):
            with console.status("Excluding items from BOM..."):
                self._chk_bom.uncheck_by_click_input()
            log.logger.info("Excluded selected products from BOM.")
        else:
            log.logger.warning(
                "Cannot exclude items from the BOM: Tab 'Product' is not visible."
            )

    def _get_window_children(self) -> None:
        """Assigns the window elements to the appropriate properties."""
        assert self._window is not None
        for child in self._window.children():
            if child.window_text() == resource.applied_keywords.props_tab_product:
                self._tab_product = TabControlWrapper(child)
            if child.window_text() == resource.applied_keywords.props_node_ok:
                self._btn_ok = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.props_node_apply:
                self._btn_apply = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.props_node_close:
                self._btn_close = ButtonWrapper(child)
            if child.window_text() == resource.applied_keywords.props_node_bom:
                self._chk_bom = ButtonWrapper(child)
        if all(
            [
                self._btn_ok,
                self._btn_apply,
                self._btn_close,
                self._tab_product,
                self._chk_bom,
            ]
        ):
            self._product_tab_visible = True

    @property
    def product_tab_visible(self) -> bool:
        return self._product_tab_visible

    @property
    def btn_ok(self) -> ButtonWrapper:
        assert self._btn_ok is not None
        return self._btn_ok

    @property
    def btn_apply(self) -> ButtonWrapper:
        assert self._btn_apply is not None
        return self._btn_apply

    @property
    def btn_close(self) -> ButtonWrapper:
        assert self._btn_close is not None
        return self._btn_close

    @property
    def chk_bom(self) -> ButtonWrapper:
        assert self._chk_bom is not None
        return self._chk_bom
