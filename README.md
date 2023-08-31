# pytia reorder tree

A python app for reordering the graph tree from a CATIA V5 product.

![state](https://img.shields.io/badge/State-beta-brown.svg?style=for-the-badge)
![version](https://img.shields.io/badge/Version-0.1.1-orange.svg?style=for-the-badge)

[![python](https://img.shields.io/badge/Python-3.10-blue.svg?style=for-the-badge)](https://www.python.org/downloads/)
![catia](https://img.shields.io/badge/CATIA-V5%206R2017-blue.svg?style=for-the-badge)
![OS](https://img.shields.io/badge/OS-WIN10%20|%20WIN11-blue.svg?style=for-the-badge)

> ⚠️ The layout of this app is heavily biased towards the workflow and needs of my companies' engineering team. Although almost everything can be changed via config files and presets, the apps basic functionality is built to work in the environment of said company.

> ⚠️ Due to lack of an API based implementation of the reorder graph tree command, the app uses a window based approach. This may result in unexpected behavior when using the app.

Check out the pytia ecosystem:

- **pytia** ([web](https://pytia.deloarts.com/), [repo](https://github.com/deloarts/pytia)): The heart of this project.
- **pytia-property-manager** ([web](https://pytia.deloarts.com/property-manager/v0.html), [repo](https://github.com/deloarts/pytia-property-manager)) : An app to edit part and product properties.
- **pytia-bounding-box** ([web](https://pytia.deloarts.com/bounding-box/v0.html), [repo](https://github.com/deloarts/pytia-bounding-box)): For retrieving the bounding box of a part.
- **pytia-reorder-tree** ([web](https://pytia.deloarts.com/bill-of-material/v0.html), [repo](https://github.com/deloarts/pytia-reorder-tree)): Exports the bill of material and data of a product.
- **pytia-title-block** ([web](https://pytia.deloarts.com/title-block/v0.html), [repo](https://github.com/deloarts/pytia-title-block)): An app to edit a drawing's title block.
- **pytia-quick-export** ([web](https://pytia.deloarts.com/quick-export/v0.html), [repo](https://github.com/deloarts/pytia-quick-export)): Single file export with useful features.
- **pytia-reorder-tree** ([web](https://pytia.deloarts.com/reorder-tree/v0.html), [repo](https://github.com/deloarts/pytia-reorder-tree)): Brings order in your product graph tree.
- **pytia-ui-tools** ([web](https://pytia.deloarts.com/), [repo](https://github.com/deloarts/pytia-ui-tools)): A toolbox for all pytia apps.

Table of contents:

- [pytia reorder tree](#pytia-reorder-tree)
  - [1 installation](#1-installation)
  - [2 setup](#2-setup)
    - [2.1 resource files](#21-resource-files)
      - [2.1.1 default files](#211-default-files)
      - [2.1.2 sample files](#212-sample-files)
      - [2.1.3 static files](#213-static-files)
    - [2.3 provide a release folder](#23-provide-a-release-folder)
    - [2.4 build](#24-build)
    - [2.5 release](#25-release)
    - [2.6 docs](#26-docs)
  - [3 usage](#3-usage)
  - [4 workspace](#4-workspace)
  - [5 developing](#5-developing)
    - [5.1 repository](#51-repository)
      - [5.1.1 cloning](#511-cloning)
      - [5.1.2 main branch protection](#512-main-branch-protection)
      - [5.1.3 branch naming convention](#513-branch-naming-convention)
      - [5.1.4 issues](#514-issues)
    - [5.2 poetry](#52-poetry)
      - [5.2.1 setup](#521-setup)
      - [5.2.2 install](#522-install)
      - [5.2.3 tests](#523-tests)
    - [5.3 pre-commit hooks](#53-pre-commit-hooks)
    - [5.4 docs](#54-docs)
    - [5.5 new revision checklist](#55-new-revision-checklist)
  - [6 license](#6-license)
  - [7 changelog](#7-changelog)
  - [8 to dos](#8-to-dos)

## 1 installation

> ✏️ For a guided installation visit [https://pytia.deloarts.com](https://pytia.deloarts.com/installation/v0.html)

On the users machine you need to install the following:

- CATIA
- [Python](https://www.python.org/downloads/)
- [Git](https://gitforwindows.org/)

When the user starts the app it will automatically install all its requirements. Further the app also updates outdated dependencies if needed. The apps environment will be created in the users appdata-folder: `C:\Users\User\AppData\Roaming\pytia\pytia_reorder_tree`

Recommended python install options for the user:

```powershell
python-installer.exe /passive PrependPath=1 Include_doc=0 Include_test=0 SimpleInstall=1 SimpleInstallDescription="python for pytia"
```

For convenience there is a powershell script that will install the required python version for you, see [assets/python_installer.ps1](assets/python_installer.ps1).

## 2 setup

### 2.1 resource files

All configuration is done via json files inside the [resources folder](/pytia_reorder_tree/resources/).

#### 2.1.1 default files

You can leave the default configuration if it suits your needs, but you can always copy any default json file, rename (get rid of 'default') it and edit its content.

Example: If you want to change the content of the [properties.default.json](/pytia_reorder_tree/resources/properties.default.json) you have to copy this file, and paste it as **properties.json**. Then you can edit the content of your newly generated properties-settings file. Same for any other default-resource file.

> ✏️ For a full description of all default files, see [docs/DEFAULT_FILES.md](/docs/DEFAULT_FILES.md).

#### 2.1.2 sample files

Files that are named like **settings.sample.json** must be copied, renamed and edited. Sample files exists only for you to have a guide, of how the config file must look.

Example: Before you can build the app you have to copy the [settings.sample.json](/pytia_reorder_tree/resources/settings.sample.json) and rename it to **settings.json**. Then you can edit its content to match your requirements.

> ✏️ For a full description of all sample files, see [docs/SAMPLE_FILES.md](/docs/SAMPLE_FILES.md).

#### 2.1.3 static files

Files without 'default' or 'sample' in their names cannot be changed! Just leave them there, they are needed for the app to work.

### 2.3 provide a release folder

To be able to launch the app from within CATIA you need to provide a release folder, where the app and a launcher file are stored. Both files (the app and the launcher) will be created with the [_build.py](_build.py) script, and released to the release-folder with the [_release.py](_release.py) script.

> ❗️ Add this release folder to the **settings.json** file as value of the **paths.release** key.

### 2.4 build

> ❗️ Do not build the app with poetry! This package is not not meant to be used as an import, it should be used as an app.

To build the app and make it executable for the user run the [_build.py](_build.py) python file. The app is only built if all tests are passing. The app will be exported to the [_build-folder](/build/). Additionally to the built python-file a catvbs-file will be exported to the same build-folder. This file is required to launch the app from within CATIA, see the next chapter.

> ✏️ You can always change the name of the build by editing the value from the **files.app** key of the **settings.json**.
>
> ✏️ The reason this app isn't compiled to an exe is performance. It takes way too long to load the UI if the app isn't launched as python zipfile.

### 2.5 release

To release the app into the provided release folder run the [_release.py](_release.py) script.

To run the app from within CATIA, add the release-folder to the macro-library in CATIA. CATIA will recognize the catvbs-file, so you can add it to a toolbar.

You can always change the path of the release folder by editing the value from the **paths.release** key of the **settings.json**.

> ⚠️ Once you built and released the app you cannot move the python app nor the catvbs script to another location, because absolute paths will be written to those files. If you have to move the location of the files you have to change the paths in the **settings.json** config file, build the app again and release it to the new destination.

### 2.6 docs

You can find the documentation in the [docs folder](/docs).

## 3 usage

Use the launcher (a.k.a the catvbs-file) to launch the app. On the first run all required dependencies will be installed:

![Installer](assets/images/installer.png)

After the installation you can run the app using the launcher:

![App](assets/images/app.png)

The app runs fully automatic:

- It scans the product for existing `group identifiers` and removes them
- Then new `group identifiers` will be added by the `group` property of all children (groups are available since **v0.2.4** of the [pytia-property-manager](https://github.com/deloarts/pytia-property-manager)). This can be changed in the settings.json.
- Afterward the app reorders the graph tree by issuing the `reorder graph tree` command.

## 4 workspace

The workspace is an **optional** config file, that can be used to alter the behavior of the app. The workspace file is a yaml-file, which must be saved somewhere in the project directory, where the catia document, from which to manage the properties, is also stored:

```bash
your-fancy-project
├─── main.CATProduct
├─── subfolder-A
│    ├─── product-A.CATProduct
│    ├─── part-A-01.CATPart
│    └─── part-A-02.CATPart
├─── subfolder-B
│    ├─── product-B.CATProduct
│    ├─── part-B-01.CATPart
│    └─── part-B-02.CATPart
└─── workspace.yml
```

As long as the workspace file is located somewhere in the project, and as long as this file is in the **same** folder, or any folder **above** the CATProduct file, it will be used.

For a detailed description of the workspace config file, see [WORKSPACE_FILE](docs/WORKSPACE_FILE.md).

The filename of the workspace file can be changed in the **settings.json** file, see [SAMPLE_FILES](docs/SAMPLE_FILES.md).

## 5 developing

For developing you would, additionally to the system requirements, need to install:

- [Poetry](https://python-poetry.org/docs/master/#installation)
- [Git](https://git-scm.com/downloads) or [GitHub Desktop](https://desktop.github.com/)

### 5.1 repository

#### 5.1.1 cloning

Clone the repo to your local machine:

```powershell
cd $HOME
New-Item -Path '.\git\pytia-reorder-tree' -ItemType Directory
cd .\git\pytia-reorder-tree\
git clone git@github.com:deloarts/pytia-reorder-tree.git
```

Or use GitHub Desktop.

#### 5.1.2 main branch protection

> ❗️ Never develop new features and fixes in the main branch!

The main branch is protected: it's not allowed to make changes directly to it. Create a new branch in order work on issues. The new branch should follow the naming convention from below.

#### 5.1.3 branch naming convention

1. Use grouping tokens at the beginning of your branch names, such as:
    - feature: A new feature that will be added to the project
    - fix: For bugfixes
    - tests: Adding or updating tests
    - docs: For updating the docs
    - wip: Work in progress, won't be finished soon
    - junk: Just for experimenting
2. Use slashes `/` as delimiter in branch names (`feature/docket-export`)
3. Avoid long descriptive names, rather refer to an issue
4. Do not use bare numbers as leading parts (`fix/108` is bad, `fix/issue108` is good)

#### 5.1.4 issues

Use the issue templates for creating an issue. Please don't open a new issue if you haven't met the requirements and add as much information as possible. Further:

- Format your code in an issue correctly with three backticks, see the [markdown guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
- Add the full error trace.
- Do not add screenshots for code or traces.

### 5.2 poetry

#### 5.2.1 setup

If you prefer the environment inside the projects root, use:

```powershell
poetry config virtualenvs.in-project true
```

> ⚠️ Make sure not to commit the virtual environment to GitHub. See [.gitignore](.gitignore) to find out which folders are ignored.

#### 5.2.2 install

Install all dependencies (assuming you are inside the projects root folder):

```powershell
poetry install
```

Check your active environment with:

```powershell
poetry env list
poetry env info
```

Update packages with:

```powershell
poetry update
```

#### 5.2.3 tests

Tests are done with pytest. For testing with poetry run:

```powershell
poetry run pytest
```

> ⚠️ Test discovery in VS Code only works when CATIA is running.

### 5.3 pre-commit hooks

Don't forget to install the pre-commit hooks:

```powershell
pre-commit install
```

### 5.4 docs

Documentation is done with [pdoc3](https://pdoc3.github.io/pdoc/).

To update the documentation run:

```powershell
python -m pdoc --html --output-dir docs pytia_reorder_tree
```

For preview run:

```powershell
python -m pdoc --http : pytia_reorder_tree
```

### 5.5 new revision checklist

On a new revision, do the following:

1. Update **dependency versions** in
   - [pyproject.toml](pyproject.toml)
   - [dependencies.json](pytia_reorder_tree/resources/dependencies.json)
   - [README.md](README.md)
2. Update **dependencies**: `poetry update`
3. Update the **version** in
   - [pyproject.toml](pyproject.toml)
   - [__ init __.py](pytia_reorder_tree/__init__.py)
   - [README.md](README.md)
4. Run all **tests**: `poetry run pytest`
5. Check **pylint** output: `poetry run pylint pytia_reorder_tree/`
6. Update the **documentation**: `poetry run pdoc --force --html --output-dir docs pytia_reorder_tree`
7. Update the **lockfile**: `poetry lock`
8. Update the **requirements.txt**: `poetry export --with dev -f requirements.txt -o requirements.txt`

## 6 license

[MIT License](LICENSE)

## 7 changelog

**v0.1.1**: Run `hide from bom` command last.  
**v0.1.0**: Initial commit.  

## 8 to dos

Using VS Code [Comment Anchors](https://marketplace.visualstudio.com/items?itemName=ExodiusStudios.comment-anchors) to keep track of to-dos.
