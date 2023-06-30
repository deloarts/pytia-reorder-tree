# sample files

Explains the config of all sample files.

All sample files must be copied, renamed and edited to fit your needs.

## 1 settings.sample.json

This file contains the basic settings for the app.

- **Location**: [/pytia_reorder_tree/resources/settings.sample.json](../pytia_reorder_tree/resources/settings.sample.json)
- **Rename to**: `settings.json`

### 1.1 file content

```json
{
    "title": "PYTIA Reorder Tree",
    "debug": false,
    "restrictions": {
        "allow_all_users": false,
        "allow_all_editors": false,
        "allow_outside_workspace": true
    },
    "paths": {
        "catia": "C:\\CATIA\\V5-6R2017\\B27",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_reorder_tree.pyz",
        "launcher": "pytia_reorder_tree.catvbs",
        "workspace": "workspace.yml"
    },
    "tree": {
        "create_groups": true,
        "group_prefix": "GROUP ",
        "group_postfix": "",
        "IN_delimiter": " | ",
        "IN_position": 1
    },
    "urls": {
        "help": "https://github.com/deloarts/pytia-reorder-tree"
    },
    "mails": {
        "admin": "admin@company.com"
    }
}
```

### 1.2 description

name | type | description
--- | --- | ---
title | `str` | The apps title. This will be visible in the title bar of the window.
debug | `bool` | The flag to declare the debug-state of the app. The app cannot be built if this value is true.
restrictions.allow_all_users | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users from the **users.json** file can modify the properties.
restrictions.allow_all_editors | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users which are declared in the **workspace** file can modify the properties. If no workspace file is found, or no **editors** list-item is inside the workspace file, then this is omitted, and everyone can make changes.
restrictions.allow_outside_workspace | `bool` | If set to `false` a **workspace** file must be provided somewhere in the folder structure where the document is saved. This also means, that an unsaved document (a document which doesn't have a path yet) cannot be modified.
paths.catia | `str` | The absolute path to the CATIA executables. Environment variables will be expanded to their respective values. E.g: `%ONEDRIVE%\\CATIA\\Apps` will be resolved to `C:\\Users\\...\\OneDrive\\CATIA\\Apps`.
paths.release | `str` | The folder where the launcher and the app are released into. Environment variables will be expanded to their respective values. E.g: `%ONEDRIVE%\\CATIA\\Apps` will be resolved to `C:\\Users\\...\\OneDrive\\CATIA\\Apps`.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
files.workspace | `str` | The name of the workspace file.
tree.create_groups | `bool` | Flag for creating groups during reordering.
tree.group_prefix | `str` | Possibility for adding a prefix to the group identifier. Uses the group property from pytia-property-manager.
tree.group_postfix | `str` | Possibility for adding a postfix to the group identifier. Uses the group property from pytia-property-manager.
tree.IN_delimiter | `str` | The delimiter for recognizing the instance number in the graph tree node. Example: If the tree node string looks like this `#PN# , #IN# , #SO#` then the delimiter is `' , '` and the position is '1'.
tree.IN_position | `int` | The position of the instance number in the tree node, see example above.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mails.admin | `str` | The mail address of the sys admin. Required for error mails.

## 2 users.sample.json

This file contains a list of users known to the system.

- **Location**: [/pytia_reorder_tree/resources/users.sample.json](../pytia_reorder_tree/resources/users.sample.json)
- **Rename to**: `users.json`

### 2.1 file content

```json
[
    {
        "logon": "admin",
        "id": "001",
        "name": "Administrator",
        "mail": "admin@company.com"
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
logon | `str` | The windows logon name of the user.
id | `str` | The ID of the user. Can be used for the employee ID.
name | `str` | The name of the user.
mail | `str` | The users mail address.

## 3 docket.sample.json

This file contains the configuration for the docket export.

> ⚠️ This config file will be documented later, as the docket generation will be changed in the future (it's currently a very hacky solution).

- **Location**: [/pytia_reorder_tree/resources/docket.sample.json](../pytia_reorder_tree/resources/users.sample.json)
- **Rename to**: `docket.json`
