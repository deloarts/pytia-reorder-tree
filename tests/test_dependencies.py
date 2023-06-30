"""
    Test the dependencies versions.
"""

import json
import os

import toml

directory = os.path.dirname(os.path.realpath("__file__"))


def test_versions():
    """Test if the versions from the pyproject file are matching the versions of the deps json."""
    with open(
        os.path.join(directory, "pytia_reorder_tree\\resources\\dependencies.json"),
        "r",
    ) as f:
        deps = json.load(f)

    with open(os.path.join(directory, "pyproject.toml"), "r") as f:
        pyproject = dict(toml.load(f)["tool"]["poetry"]["dependencies"])
        pyproject.pop("python")

    assert len(deps) == len(pyproject)

    for item in deps:
        if item["name"] == "pytia":
            assert f"v{item['version']}" == pyproject["pytia"]["tag"]
        if item["name"] == "pytia_ui_tools":
            assert f"v{item['version']}" == pyproject["pytia-ui-tools"]["tag"]
        if item["name"] == "comtypes":
            assert item["version"] == pyproject["comtypes"]
        if item["name"] == "pywinauto":
            assert item["version"] == pyproject["pywinauto"]
        if item["name"] == "rich":
            assert item["version"] == pyproject["rich"]


def test_imports():
    """Tests if no third party imports are in the dependencies file."""
    with open(
        os.path.join(directory, "pytia_reorder_tree\\dependencies.py"),
        "r",
    ) as f:
        for line in f.readlines():
            assert "pytia" not in line
            assert "pytia_ui_tools" not in line
