# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import date

__all__ = [
    "__version__",
    "__description__",
    "__keywords__",
    "__author__",
    "__author_email__",
    "__url__",
    "__platforms__",
    "__license__",
    "__classifiers__",
    "__install_requires__",
    "__zip_safe__",
    "__copyright__",
]

__version__ = "0.2.1"
__description__ = "nimbus_chart"
__keywords__ = ["nimbus_chart", "nimbus", "chart"]

__author__ = "william"
__author_email__ = "william.ren@live.cn"
__url__ = "https://github.com/williamren"
__platforms__ = "Any"
__license__ = "Apache License 2.0"
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django :: 1.8",
    "Framework :: Django :: 1.9",
    "Framework :: Django :: 1.10",
    "Framework :: Django :: 1.11",
    "Topic :: Internet :: WWW/HTTP",
]
__install_requires__ = [
    "Django",
    "jupyter-pip>=0.3.1",
    "pyecharts>=0.5.9",
    "pyecharts_javascripthon",
]
__zip_safe__ = False
__copyright__ = "Copyright 2001-{0} {1}".format(date.today().year, __author__)
