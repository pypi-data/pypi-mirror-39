# -*- coding: utf-8 -*-

import os
import io
import re
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    f = read(*file_paths)
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f, re.M)
    if m:
        return m.group(1)
    raise RuntimeError("Unable to find version string.")


def find_author(*file_paths):
    f = read(*file_paths)
    m = re.search(r"^__author__ = ['\"]([^'\"]*)['\"]", f, re.M)
    if m:
        return m.group(1)
    raise RuntimeError("Unable to find author string.")


setup(	name="bklv2",
        version=find_version( "bklv2", "__init__.py" ),
        url="https://github.com/etecor/bklv2",
        description="Backlog API v2 library",
        long_description=open('README.md', encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        author=find_author( "bklv2", "__init__.py" ),
        license="MIT",
        packages=["bklv2"],
        install_requires=["rfc6266", "requests"],
        classifiers=[
            #"Development Status :: 1 - Planning",
            "Development Status :: 2 - Pre-Alpha",
            #"Development Status :: 3 - Alpha",
            #"Development Status :: 4 - Beta",
            #"Development Status :: 5 - Production/Stable",
            #"Development Status :: 6 - Mature",
            #"Development Status :: 7 - Inactive",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
    )
