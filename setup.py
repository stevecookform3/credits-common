#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import setuptools

packages = [
    "base58==0.2.2",
    "ed25519",
    "logbook==0.12.5",
]

setuptools.setup(
    name="credits.common",
    version="1.0.0",
    author="Credits Developers",
    packages=setuptools.find_packages(),
    install_requires=packages,
    author_email="admin@credits.vision",
    namespace_packages=['credits']
)
