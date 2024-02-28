"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Tk


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass for the main windows variables."""

    status: StringVar
    task: IntVar

    def __init__(self, root: Tk) -> None:
        """
        Inits the variables.

        Args:
            root (Tk): The main window.
        """
        self.status = StringVar(master=root, name="status", value="Loading application")
        self.task = IntVar(master=root, name="task", value=0)
