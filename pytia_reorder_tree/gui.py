"""
    The main window for the application.
"""

import tkinter as tk
from pathlib import Path
from tkinter import font
from tkinter import messagebox as tkmsg

import ttkbootstrap as ttk
from app.frames import Frames
from app.layout import Layout
from app.traces import Traces
from app.vars import Variables
from const import APP_VERSION
from const import LOG
from const import LOGS
from exceptions import WarningError
from pytia.exceptions import PytiaBodyEmptyError
from pytia.exceptions import PytiaDifferentDocumentError
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.exceptions import PytiaNoDocumentOpenError
from pytia.exceptions import PytiaPropertyNotFoundError
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia_ui_tools.exceptions import PytiaUiToolsOutsideWorkspaceError
from pytia_ui_tools.handlers.error_handler import ErrorHandler
from pytia_ui_tools.handlers.mail_handler import MailHandler
from pytia_ui_tools.window_manager import WindowManager
from resources import resource
from task import Task


class GUI(tk.Tk):
    """The user interface of the app."""

    WIDTH = 360
    HEIGHT = 75

    def __init__(self) -> None:
        """Inits the main window."""
        ttk.tk.Tk.__init__(self)
        self.style = ttk.Style(theme="darkly")

        # CLASS VARS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.vars = Variables(root=self)
        self.frames = Frames(root=self)
        self.layout = Layout(
            root=self,
            frames=self.frames,
            variables=self.vars,
        )

        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        # UI TOOLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.window_manager = WindowManager(self)
        self.mail_handler = MailHandler(
            standard_receiver=resource.settings.mails.admin,
            app_title=resource.settings.title,
            app_version=APP_VERSION,
            logfile=Path(LOGS, LOG),
        )
        self.error_handler = ErrorHandler(
            mail_handler=self.mail_handler,
            warning_exceptions=[
                WarningError,
                PytiaNoDocumentOpenError,
                PytiaWrongDocumentTypeError,
                PytiaBodyEmptyError,
                PytiaPropertyNotFoundError,
                PytiaDifferentDocumentError,
                PytiaDocumentNotSavedError,
                PytiaUiToolsOutsideWorkspaceError,
            ],
        )

        # UI INIT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.title(
            f"{resource.settings.title} "
            f"{'(DEBUG MODE)' if resource.settings.debug else APP_VERSION}"
            f"{' (READ ONLY)' if self.readonly else ''}"
        )
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
        self.resizable(False, False)
        self.config(cursor="wait")
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=9)
        self.report_callback_exception = self.error_handler.exceptions_callback

        x_coordinate = int((self.winfo_screenwidth() / 2) - (GUI.WIDTH / 2))
        y_coordinate = resource.settings.top
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}+{x_coordinate}+{y_coordinate}")
        self.minsize(width=GUI.WIDTH, height=GUI.HEIGHT)

        self.update()
        self.window_manager.remove_window_buttons()

    def run(self) -> None:
        """Run the app."""
        self.after(100, self.run_controller)
        self.mainloop()

    def run_controller(self) -> None:
        """Runs all controllers. Initializes all lazy loaders, bindings and traces."""
        self.traces()

        task = Task(root=self, vars=self.vars)
        task.run()

    def traces(self) -> None:
        """Instantiates the traces class."""
        Traces(
            root=self,
            variables=self.vars,
            layout=self.layout,
        )
