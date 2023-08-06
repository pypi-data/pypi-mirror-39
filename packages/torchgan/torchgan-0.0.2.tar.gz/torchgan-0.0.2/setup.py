#!/usr/bin/env python
import os
import io
import re
import shutil
import sys
from setuptools import setup, find_packages
from pkg_resources import get_distribution, DistributionNotFound

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

readme = open('README.md').read()

VERSION = find_version('torchgan', '__init__.py')

requirements = [
    'numpy',
    'torch',
    'torchvision',
]

setup(
    # Metadata
    name='torchgan',
    version=VERSION,
    author='Avik Pal & Aniket Das',
    author_email='torchgan@gmail.com',
    url='https://github.com/torchgan/torchgan',
    description='Research Framework for easy and efficient training of GANs based on Pytorch',
    long_description=readme,
    license='MIT',

    # Package info
    packages=find_packages(exclude=('test',)),

    zip_safe=True,
    install_requires=requirements,
)
