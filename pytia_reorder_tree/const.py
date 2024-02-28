"""Constants for the app."""

import os
from pathlib import Path

__version__ = "0.1.2"

PYTIA = "pytia"
PYTIA_REORDER_TREE = "pytia_reorder_tree"

APP_NAME = "Reorder Tree"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME")).lower()
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
TEMP_EXPORT = Path(TEMP, PYTIA_REORDER_TREE, "export")
TEMP_TEMPLATES = Path(TEMP, PYTIA_REORDER_TREE, "templates")
APPDATA = Path(str(os.environ.get("APPDATA")), PYTIA, PYTIA_REORDER_TREE)
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{PYTIA_REORDER_TREE}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = Path(VENV, "Scripts\\python.exe")
VENV_PYTHONW = Path(VENV, "Scripts\\pythonw.exe")
PY_VERSION = Path(APPDATA, "pyversion.txt")

PROP_NO_BOM = "pytia.no_bom"
PROP_GROUP_IDENTIFIER = "pytia.group_identifier"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_KEYWORDS = "keywords.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_USERS = "users.json"

WEB_PIP = "https://www.pypi.org"

LOG_FORMAT = "%(message)s"

STEPS = 4
