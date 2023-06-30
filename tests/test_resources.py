"""
    Test the resources.py file.
"""

import os
from pathlib import Path

import validators


def test_resources_class():
    from pytia_reorder_tree.resources import Resources

    resource = Resources()


def test_settings():
    from pytia_reorder_tree.resources import resource

    assert isinstance(resource.settings.title, str)
    assert len(resource.settings.title) > 0
    assert isinstance(resource.settings.debug, bool)

    assert isinstance(resource.settings.restrictions.allow_all_users, bool)
    assert isinstance(resource.settings.restrictions.allow_all_editors, bool)
    assert isinstance(resource.settings.restrictions.allow_outside_workspace, bool)

    assert isinstance(resource.settings.paths.catia, Path)
    assert isinstance(resource.settings.paths.release, Path)

    assert isinstance(resource.settings.files.app, str)
    assert isinstance(resource.settings.files.launcher, str)
    assert isinstance(resource.settings.files.workspace, str)

    assert isinstance(resource.settings.tree.create_groups, bool)
    assert isinstance(resource.settings.tree.group_prefix, str)
    assert isinstance(resource.settings.tree.group_postfix, str)
    assert isinstance(resource.settings.tree.IN_delimiter, str)
    assert isinstance(resource.settings.tree.IN_position, int)

    if resource.settings.urls.help:
        assert validators.url(resource.settings.urls.help)  # type: ignore
    assert validators.email(resource.settings.mails.admin)  # type: ignore


def test_properties():
    from pytia_reorder_tree.resources import resource

    assert "project" in resource.props.keys
    assert "machine" in resource.props.keys
    assert "creator" in resource.props.keys
    assert "modifier" in resource.props.keys


def test_users():
    from pytia_reorder_tree.resources import resource

    logon_list = []

    for user in resource.users:
        assert isinstance(user.logon, str)
        assert isinstance(user.id, str)
        assert isinstance(user.name, str)
        assert isinstance(user.mail, str)
        assert user.logon not in logon_list

        logon_list.append(user.logon)


def test_release_folder():
    from pytia_reorder_tree.resources import resource

    assert os.path.isdir(resource.settings.paths.release)


def test_debug_mode():
    from pytia_reorder_tree.resources import resource

    assert resource.settings.debug == False
