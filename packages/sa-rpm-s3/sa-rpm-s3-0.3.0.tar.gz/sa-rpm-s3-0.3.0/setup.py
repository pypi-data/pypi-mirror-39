#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'sa-rpm-s3'
DESCRIPTION = 'This small tool allows you to maintain YUM repositories of RPM packages on S3. The advantage of this tool is that it does not need a full copy of the repo to operate. Just give it the new package to add, and it will just update the repodata metadata, and upload the given rpm file.'
URL = 'https://github.com/Voronenko/rpm-s3'
EMAIL = 'git@voronenko.info'
AUTHOR = 'Cyril Rohr - Portions (c) 2013, rockpack ltd, light mods by Vyacheslav Voronenko'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

REQUIRED = ['boto3 >= 1.4.4', 'pexpect']

with open('version.txt', 'r') as versionfile:
    VERSION = versionfile.read().replace('\n', '')

setup(
    name=NAME,
    version=VERSION,
    packages=['rpm_s3'],
    include_package_data=True,
    scripts=['rpm-s3'],
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    install_requires=REQUIRED
)

