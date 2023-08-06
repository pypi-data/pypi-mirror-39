# xdgspec Python package

[![pipeline status](https://gitlab.com/nobodyinperson/python3-xdgspec/badges/master/pipeline.svg)](https://gitlab.com/nobodyinperson/python3-xdgspec/commits/master)
[![coverage report](https://gitlab.com/nobodyinperson/python3-xdgspec/badges/master/coverage.svg)](https://nobodyinperson.gitlab.io/python3-xdgspec/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://nobodyinperson.gitlab.io/python3-xdgspec/)
[![PyPI](https://badge.fury.io/py/xdgspec.svg)](https://badge.fury.io/py/xdgspec)

`xdgspec` is a simple Python package to provide **convenient** access to the
variables defined in the [XDG Base Directory
Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).


## What can `xdgspec` do?

With `xdgspec` you can:

### Access the [XDG Base Directory variables](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#variables) with Appropriate Fallbacks

```python
from xdgspec import XDGDirectory
print(XDGDirectory("XDG_CONFIG_HOME").path)
print(XDGDirectory("XDG_CACHE_HOME").path)
print(XDGDirectory("XDG_DATA_HOME").path)
# ...
```

### Use a Context Manager to Automatically Create One of the [XDG Base Directories](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#basics) if it doesn't exist

```python
from xdgspec import XDGDirectory
with XDGDirectory("XDG_CONFIG_HOME") as path:
    print("{} is now definitely existing".format(path))
```

### Access and Create Package Directories

```python
from xdgspec import XDGPackageDirectory
with XDGPackageDirectory("XDG_CONFIG_HOME","mypackage") as path:
    # path = ~/.config/mypackage
    print("{} is now definitely existing".format(path))
```

### Loop Over Existing XDG System Directories

```python
from xdgspec import XDGDirectories
# variable content
print(XDGDirectories("XDG_CONFIG_DIRS").paths)
# generator of actually existing, unique directories
print(list(XDGDirectories("XDG_CONFIG_DIRS").existing_paths))
```

## Installation

The `xdgspec` package is best installed via `pip`. Run from anywhere:

```bash
python3 -m pip install --user xdgspec
```

This downloads and installs the package from the [Python Package
Index](https://pypi.org).

You may also install `xdgspec` from the repository root:

```bash
python3 -m pip install --user .
```

## Documentation

Documentation of the `xdgspec` package can be found [here on
GitLab](https://nobodyinperson.gitlab.io/python3-xdgspec/).
