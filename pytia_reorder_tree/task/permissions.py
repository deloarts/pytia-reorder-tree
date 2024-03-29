"""
    Permissions submodule.
    Checks permissions from the settings.
"""

from const import LOGON
from exceptions import WarningError
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource


class Permissions:
    """Permissions class."""

    def __init__(self, workspace: Workspace) -> None:
        """Inits the class.

        Args:
            workspace (Workspace): The pytia workspace instance.
        """
        self.workspace = workspace

    def check_user_permissions(self) -> None:
        """
        Checks if the current user can make changes with the app.
        Checks against the users set in the settings.json.
        """
        if (
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        ):
            raise WarningError(
                "You are not allowed to reorder the graph tree: Your logon "
                f"name ({LOGON}) doesn't exist in the user configuration."
            )

    def check_editor_permissions(self) -> None:
        """
        Checks if the current user can make changes with the app.
        Checks against the users set in the workspace file.
        """
        if (
            self.workspace.elements.editors
            and LOGON not in self.workspace.elements.editors
            and not resource.settings.restrictions.allow_all_editors
        ):
            raise WarningError(
                "You are not allowed to reorder the graph tree: Your logon "
                f"name ({LOGON}) doesn't exist in the workspace configuration."
            )

    def check_workspace_permissions(self) -> None:
        """Checks if workspace is enabled."""
        if not self.workspace.elements.active:
            raise WarningError(
                "This workspace is disabled. "
                "You cannot make changes in this document."
            )
