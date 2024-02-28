#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Main module for the app.
"""

import atexit
import os

from const import APP_VERSION
from const import LOGS
from const import PID
from const import PID_FILE
from dependencies import deps


def main() -> None:
    """Application entry point."""

    # For the apps auto-install-feature, all required dependencies must be
    # imported after they have been checked.
    # So: First check if all required dependencies are installed.
    # Afterwards import those modules which depend on third party modules.
    deps.install_dependencies()

    from gui import GUI  # pylint: disable=C0415
    from pytia.log import log  # pylint: disable=C0415

    with open(PID_FILE, "w") as f:
        f.write(str(PID))
    atexit.register(lambda: os.remove(PID_FILE))

    os.makedirs(LOGS, exist_ok=True)

    log.set_level_warning()
    log.info(f"Running PYTIA Reorder Tree {APP_VERSION}, PID={PID}")

    gui = GUI()
    gui.run()


if __name__ == "__main__":
    main()
