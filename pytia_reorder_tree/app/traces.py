"""
    Traces submodule for the app.
"""

from tkinter import Tk

from app.layout import Layout
from app.vars import Variables
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from ttkbootstrap import Style


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(
        self,
        root: Tk,
        variables: Variables,
        layout: Layout,
    ) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
            doc_helper(LazyDocumentHelper): The lazy doc loader instance.
        """
        self.root = root
        self.vars = variables
        self.layout = layout

        self._add_traces()
        log.info("Traces initialized.")

    def _add_traces(self) -> None:
        """Adds all traces."""
        self.vars.status.trace_add("write", self.trace_status)
        self.vars.task.trace_add("write", self.trace_task)

    def trace_status(self, *_) -> None:
        self.root.update()

    def trace_task(self, *_) -> None:
        self.layout.task_meter.configure(amountused=self.vars.task.get())
        self.root.update()
