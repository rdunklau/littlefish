#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 by Ronan Dunklau, Kozea
# This file is part of multicorn-demo, licensed under a 3-clause BSD license.

"""
A demo for multicorn
"""

from setuptools import setup, find_packages

options = dict(
    name="littlefish",
    version="0.0.1",
    description="",
    long_description=__doc__,
    author="Ronan Dunklau",
    author_email="ronan@dunklau.fr",
    license="BSD",
    platforms="Any",
    packages=find_packages(),
    install_requires=["flask>=0.8", 'flask-sqlalchemy', 'Flask-WTF', 'psycopg2'],
    classifiers=[
        "Development Status :: WIP",
        "Intended Audience :: Public",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Linux",
        "Programming Language :: Python :: 2.7"])

setup(**options)
