"""
    The layout of the app.
"""

from tkinter import Tk

from app.frames import Frames
from app.vars import Variables
from const import STEPS
from PIL import Image
from ttkbootstrap import Label
from ttkbootstrap import Meter

# ttkbootstrap uses the deprecated Image.CUBIC, so we need to specify Image.BICUBIC
# in order for the Meter to work
Image.CUBIC = Image.BICUBIC  # type: ignore


class Layout:
    """The layout class of the app, holds all widgets."""

    MARGIN_X = 10
    MARGIN_Y = 10

    def __init__(self, root: Tk, frames: Frames, variables: Variables) -> None:
        """
        Inits the Layout class. Creates and places the widgets of the main window.

        Args:
            root (Tk): The main window.
            frames (Frames): The frames of the main window.
            variables (Variables): The variables of the main window.
        """

        # region FRAME Infra ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._task_meter = Meter(
            master=frames.infrastructure,
            metersize=50,
            amounttotal=STEPS,
            amountused=1,
            metertype="semi",
            interactive=False,
            showtext=False,
            bootstyle="danger",
            # padding=1,
        )
        self._task_meter.grid(
            row=0,
            column=0,
            padx=(10, 10),
            pady=(10, 10),
            sticky="nsew",
            rowspan=2,
        )

        lbl_status_text = Label(frames.infrastructure, text="Reordering graph tree")
        lbl_status_text.grid(row=0, column=1, padx=(5, 5), pady=(10, 1), sticky="nsw")

        lbl_status_value = Label(frames.infrastructure, textvariable=variables.status)
        lbl_status_value.grid(row=1, column=1, padx=(5, 5), pady=(1, 15), sticky="nsw")

        # endregion

    @property
    def task_meter(self) -> Meter:
        return self._task_meter
