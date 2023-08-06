# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys
import re
import codecs
import shutil
import logging
from io import open
from datetime import date, datetime, time, timedelta
from distutils.util import convert_path
from setuptools import (
    setup,
    PackageFinder,
    PEP420PackageFinder,
    find_packages as setup_find_packages,
    findall as setup_findall,
)

logger = logging.getLogger(__name__)

try:
    from pypandoc import convert
    def read_md(f):
        return convert(f, 'rst')
except Exception as e:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


class SetupPackageFinder(PackageFinder):

    @classmethod
    def find(cls, where='.', prefix=None, exclude=(), include=('*',)):
        paths = list(cls._find_packages_iter(
            convert_path(where),
            cls._build_filter('ez_setup', '*__pycache__', *exclude),
            cls._build_filter(*include)))
        if prefix is not None:
            paths = [os.path.relpath(path, prefix) for path in paths]
        return paths

    @classmethod
    def find_data(cls, where='.', prefix=None, exclude=(), include=('*',)):
        package = os.path.basename(where)
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


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


