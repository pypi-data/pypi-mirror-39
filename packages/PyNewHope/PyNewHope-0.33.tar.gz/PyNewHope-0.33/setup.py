#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def read_(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="PyNewHope",
    version="0.33",
    packages=["pynewhope"],
    author="Scott Wyman Neagle, Svetlin Nakov",
    description=(
        "An experimental implementation of the NewHope post-quantum key exchange algorithm"),
    license="MIT",
    keywords=["NewHope", "PQC", "post-quantum-cryptography", "key-exchange", "cryptography"],
    url="https://github.com/nakov/PyNewHope",
    download_url = "http://www.nakov.com",
    long_description=read_("README.md"),
    long_description_content_type='text/markdown'
)
