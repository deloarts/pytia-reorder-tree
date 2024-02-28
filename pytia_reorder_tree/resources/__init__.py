"""
    Loads the content from config files.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import atexit
import importlib.resources
import json
import os
import tkinter.messagebox as tkmsg
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Protocol

from const import APP_VERSION
from const import APPDATA
from const import CONFIG_APPDATA
from const import CONFIG_KEYWORDS
from const import CONFIG_PROPS
from const import CONFIG_PROPS_DEFAULT
from const import CONFIG_SETTINGS
from const import CONFIG_USERS
from const import LOGON
from resources.utils import expand_env_vars


class DataclassProtocol(Protocol):
    __dataclass_fields__: Dict


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsExport:
    """Dataclass for export settings."""

    apply_username_in_bom: bool
    apply_username_in_docket: bool
    lock_drawing_views: bool
    jpg_views: List[List[float]]


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsRestrictions:
    """Dataclass for restrictive settings."""

    allow_all_users: bool
    allow_all_editors: bool
    allow_outside_workspace: bool


@dataclass(slots=True, kw_only=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    catia: Path
    release: Path

    def __post_init__(self) -> None:
        self.catia = Path(expand_env_vars(str(self.catia)))
        self.release = Path(expand_env_vars(str(self.release)))


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str
    workspace: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsGroupsItem:
    """Dataclass for groups (settings.json)."""

    name: str
    value: str
    source: int


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsTree:
    """Dataclass for tree options (settings.json)."""

    create_groups: bool
    group_prefix: str
    group_postfix: str
    IN_delimiter: str
    IN_position: int
    renumber: bool
    start_index: int


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    admin: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    top: int
    restrictions: SettingsRestrictions
    paths: SettingsPaths
    files: SettingsFiles
    # groups: List[SettingsGroupsItem]
    tree: SettingsTree
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.restrictions = SettingsRestrictions(**dict(self.restrictions))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        # self.groups = [SettingsGroupsItem(**dict(i)) for i in self.groups]  # type: ignore
        self.tree = SettingsTree(**dict(self.tree))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class Props:
    """Dataclass for properties on the part (properties.json)."""

    project: str
    machine: str
    creator: str
    modifier: str
    group: str
    filter: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Props dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Props dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True)
class KeywordElements:
    """Dataclass for keyword elements."""

    partnumber: str
    reorder_cmd_name: str
    reorder_window_name: str
    reorder_node_ok: str
    reorder_node_apply: str
    reorder_node_abort: str
    reorder_node_move_up: str
    reorder_node_move_down: str
    reorder_node_list_box: str
    props_cmd_name: str
    props_window_name: str
    props_tab_product: str
    props_node_ok: str
    props_node_apply: str
    props_node_close: str
    props_node_bom: str


@dataclass
class AppliedKeywords(KeywordElements):
    ...


@dataclass(slots=True, kw_only=True)
class Keywords:
    """Dataclass for language specific keywords."""

    en: KeywordElements
    de: KeywordElements

    def __post_init__(self) -> None:
        self.en = KeywordElements(**dict(self.en))  # type: ignore
        self.de = KeywordElements(**dict(self.de))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class User:
    """Dataclass a user (users.json)."""

    logon: str
    id: str
    name: str
    mail: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the User dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the User dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True)
class AppData:
    """Dataclass for appdata settings."""

    version: str = field(default=APP_VERSION)
    counter: int = 0
    disable_volume_warning: bool = False

    def __post_init__(self) -> None:
        self.version = (
            APP_VERSION  # Always store the latest version in the appdata json
        )
        self.counter += 1


class Resources:  # pylint: disable=R0902
    """Class for handling resource files."""

    def __init__(self) -> None:
        self._language_applied = False
        self._applied_keywords: AppliedKeywords

        self._read_settings()
        self._read_props()
        self._read_keywords()
        self._read_users()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def props(self) -> Props:
        """properties.json"""
        return self._props

    @property
    def keywords(self) -> Keywords:
        """keywords.json"""
        return self._keywords

    @property
    def applied_keywords(self) -> AppliedKeywords:
        """Translated version of the keywords json."""
        if not self._language_applied:
            raise Exception("Language has not been applied to filters.json.")
        return self._applied_keywords

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_props(self) -> None:
        """Reads the props json from the resources folder."""
        props_resource = (
            CONFIG_PROPS
            if importlib.resources.is_resource("resources", CONFIG_PROPS)
            else CONFIG_PROPS_DEFAULT
        )
        with importlib.resources.open_binary("resources", props_resource) as f:
            self._props = Props(**json.load(f))

    def _read_keywords(self) -> None:
        """Reads the keywords json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_KEYWORDS) as f:
            self._keywords = Keywords(**json.load(f))

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]

    def _read_appdata(self) -> None:
        """Reads the json config file from the appdata folder."""
        if os.path.exists(appdata_file := f"{APPDATA}\\{CONFIG_APPDATA}"):
            with open(appdata_file, "r", encoding="utf8") as f:
                try:
                    value = AppData(**json.load(f))
                except JSONDecodeError:
                    value = AppData()
                    tkmsg.showwarning(
                        title="Configuration warning",
                        message="The AppData config file has been corrupted. \
                            You may need to apply your preferences again.",
                    )
                self._appdata = value
        else:
            self._appdata = AppData()

    def _write_appdata(self) -> None:
        """Saves appdata config to file."""
        os.makedirs(APPDATA, exist_ok=True)
        with open(f"{APPDATA}\\{CONFIG_APPDATA}", "w", encoding="utf8") as f:
            json.dump(asdict(self._appdata), f)

    def apply_language(self, language=Literal["en", "de"]) -> None:
        self._applied_keywords = AppliedKeywords(
            **asdict(
                resource._keywords.en if language == "en" else resource._keywords.de
            )
        )
        self._language_applied = True

    def logon_exists(self, logon: Optional[str] = None) -> bool:
        """
        Returns wether the users logon exists in the dataclass, or not. Uses the logon-value of the
        current session if logon is omitted.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for user in self._users:
            if user.logon == logon:
                return True
        return False

    def get_user_by_logon(self, logon: str) -> User:
        """
        Returns the user dataclass that matches the logon value.

        Args:
            user (str): The user to fetch from the dataclass list.

        Raises:
            ValueError: Raised when the user doesn't exist.

        Returns:
            User: The user from the dataclass list that matches the provided logon name.
        """
        for index, value in enumerate(self._users):
            if value.logon == logon:
                return self._users[index]
        raise ValueError

    def user_exists(self, logon: str) -> bool:
        """
        Returns wether the user exists in the dataclass list, or not.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        for user in self._users:
            if user.logon == logon:
                return True
        return False


resource = Resources()
