# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys
import re
import logging
from io import open
from distutils.util import convert_path
from importlib import import_module
from setuptools import (
    setup,
    PackageFinder,
    PEP420PackageFinder,
    find_packages as setup_find_packages,
    findall as setup_findall,
)

try:
    from pypandoc import convert
    def read_md(f):
        return convert(f, 'rst')
except Exception as e:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()

logger = logging.getLogger(__name__)


class SetupPackageFinder(PackageFinder):

    @classmethod
    def find(cls, where='.', prefix=None, exclude=(), include=('*',)):
        prefix = os.path.abspath(prefix) if prefix else os.path.abspath('.')
        paths = list(cls._find_packages_iter(
            convert_path(where),
            cls._build_filter('ez_setup', '*__pycache__', *exclude),
            cls._build_filter(*include)))
        if prefix is not None:
            paths = [os.path.relpath(path, prefix) for path in paths]
        paths = [path.replace(os.sep, ".") for path in paths]
        return paths

    @classmethod
    def find_data(cls, where='.', prefix=None, exclude=(), include=('*',)):
        package = os.path.basename(where)
        prefix = os.path.abspath(prefix) if prefix else os.path.abspath('.')
        package_data = []
        datas = list(cls._find_package_data_iter(
            convert_path(where),
            cls._build_filter('ez_setup', '*__pycache__', *exclude),
            cls._build_filter(*include))
        )
        if prefix is not None:
            datas = [os.path.relpath(path, prefix) for path in datas]
        for data in datas:
            package_data.append(data.replace(package + os.sep, '', 1))
        return {
            package: package_data,
        }

    @classmethod
    def _find_packages_iter(cls, where, exclude, include):
        """
        All the packages found in 'where' that pass the 'include' filter, but
        not the 'exclude' filter.
        """
        for root, dirs, files in os.walk(where, followlinks=True):
            if not cls._looks_like_package(root):
                continue
            if include(root) and not exclude(root):
                yield root

    @classmethod
    def _find_package_data_iter(cls, where, exclude, include):
        """
        All the packages found in 'where' that pass the 'include' filter, but
        not the 'exclude' filter.
        """
        for root, dirs, files in os.walk(where, followlinks=True):
            # if cls._looks_like_package(root):
            #     continue
            for file in files:
                if include(file) and not exclude(file):
                    yield os.path.join(root, file)


find_packages = SetupPackageFinder.find
find_package_data = SetupPackageFinder.find_data
_package_info = {}


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def _get_package(name, package=None):
    mod = import_module(name, package)
    return mod


def _get_package_info(name, package=None):
    global _package_info
    if _package_info:
        return _package_info
    mod = _get_package(name, package=package)
    attrs = getattr(mod, "__all__", [])
    _package_info = {attr.strip("__"): getattr(mod, attr, None) for attr in attrs}
    return _package_info


def package_attr(name, package=None, attr="version", default=""):
    info = _get_package_info(name, package=package)
    return info.get(attr, default)

