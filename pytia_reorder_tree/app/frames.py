"""
    Frames submodule for the main window.
"""

from tkinter import Tk


from ttkbootstrap import Frame


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._frame_infra = Frame(master=root)
        self._frame_infra.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

    @property
    def infrastructure(self) -> Frame:
        """Returns the infrastructure frame."""
        return self._frame_infra
