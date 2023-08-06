#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import textwrap
import subprocess
import shutil
import setuptools
import traceback


dependencies = [
    'aiofiles',
    'aiohttp',
    'async-timeout',
    'asynctest',
    'coverage',
    'docutils',
    'requests',
    'urllib3',
    'websockets',
]


with open("libneko/__init__.py") as fp:
    init_file = fp.read()
    attrs = {k: v for (k, v) in re.findall(r'^__(\w+)__ = "([^"]+)', init_file, re.M)}


def sp(c):
    return subprocess.check_output(c, shell=True, universal_newlines=True)


try:
    name = os.environ["LIBNEKO_PACKAGE_NAME"]
except KeyError:
    name = "libneko"


print("Targeting", attrs["version"], attrs.get('release', ''))

try:
    with open("README.rst") as fp:
        readme = fp.read()
except Exception:
    print("Could not read README.rst")
    traceback.print_exc()
    readme = "libneko!"


try:
    attrs.pop('release')
except:
    pass


setuptools.setup(
    name=name,
    packages=["libneko", "libneko.extras", "libneko.pag", "libneko.pag.factory",
              "libneko.test"],
    description=textwrap.dedent(
        """
        Utilities and addons for Discord.py. Check out https://koyagami.gitlab.io/libneko/ 
        for the full documentation, or https://gitlab.com/koyagami/libneko for the source.
        """
    ),
    install_requires=dependencies,
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    long_description=readme,
    long_description_content_type="text/x-rst",
    **attrs
)
