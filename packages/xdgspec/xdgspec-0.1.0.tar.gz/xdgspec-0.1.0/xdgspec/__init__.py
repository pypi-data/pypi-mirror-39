# system modules
import logging
import os
from os.path import abspath, exists, expanduser, join

# internal modules
import xdgspec
from xdgspec.version import __version__
from xdgspec.utils import *

# external modules

logger = logging.getLogger(__name__)

XDG_HOME_DEFAULTS = {
    "XDG_DATA_HOME": expanduser(join("~", ".local", ".share")),
    "XDG_CONFIG_HOME": expanduser(join("~", ".config")),
    "XDG_CACHE_HOME": expanduser(join("~", ".cache")),
}
XDG_DIRS_DEFAULTS = {
    "XDG_DATA_DIRS": ":".join(
        (
            expanduser(join(join(os.sep, "usr"), "local", "share")),
            expanduser(join(join(os.sep, "usr"), "share")),
        )
    ),
    "XDG_CONFIG_DIRS": expanduser(join(join(os.sep, "etc"), "xdg")),
}
XDG_DEFAULTS = XDG_HOME_DEFAULTS.copy()
XDG_DEFAULTS.update(XDG_DIRS_DEFAULTS)

locals().update(XDG_HOME_DEFAULTS)
locals().update(XDG_DIRS_DEFAULTS)


class XDGDirectoryVariable:
    def __init__(self, name, defaults=XDG_DEFAULTS):
        self.defaults = defaults
        self.name = name

    @property
    def name(self):  # pragma: no cover
        try:
            self._name
        except AttributeError:
            self._name = ""
        return self._name

    @name.setter
    def name(self, new):
        new = str(new)
        if new not in self.defaults:
            raise ValueError(
                "Invalid name '{}'. Use one of {}.".format(
                    new, ", ".join(map("'{}'".format, self.defaults.keys()))
                )
            )
        self._name = new

    @property
    def value(self):
        return os.environ.get(
            self.name, XDG_DEFAULTS.get(self.name)
        ) or XDG_DEFAULTS.get(self.name)

    def __str__(self):
        return str(self.value)


class Directory:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if not exists(self.path):
            logger.info("Create nonexistent directory '{}'".format(self.path))
            os.makedirs(self.path)
        return self.path

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        return str(self.path)


class XDGDirectory(XDGDirectoryVariable, Directory):
    def __init__(self, name):
        XDGDirectoryVariable.__init__(
            self, name=name, defaults=XDG_HOME_DEFAULTS
        )

    @property
    def path(self):
        return expanduser(self.value)


class XDGPackageDirectory(XDGDirectory):
    def __init__(self, name, packagename=__name__.split(".")[0]):
        XDGDirectory.__init__(self, name)
        self.packagename = packagename

    @property
    def path(self):
        return join(expanduser(self.value), self.packagename)


class XDGDirectories(XDGDirectoryVariable):
    def __init__(self, name):
        XDGDirectoryVariable.__init__(
            self, name=name, defaults=XDG_DIRS_DEFAULTS
        )

    @property
    def paths(self):
        return self.value.split(":")

    @property
    def existing_paths(self):
        return filter(
            exists,
            unique(filter(lambda p: abspath(expanduser(p)), self.paths)),
        )

    def __iter__(self):
        return self.existing_paths
