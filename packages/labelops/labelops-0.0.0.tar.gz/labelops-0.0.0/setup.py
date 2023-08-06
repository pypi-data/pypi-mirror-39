#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import sys

here = path.abspath(path.dirname(__file__))

long_description = "A package to handle specific operations on neuronal meshes with labeled data, including compressing and decompressing those labels."

# read in version number
with open(path.join(here, 'labelops', 'version.py')) as f:
    exec(f.read())

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split()

setup(
    name='labelops',
    version=__version__,
    description="Operates on labeled neuronal meshes.",
    long_description=long_description,
    author='Christos Papadopoulos',
    author_email='cpapa97@gmail.com',
    license="GNU LGPL",
    url='https://github.com/Cajal/LabelOps',
    keywords='functional connectomics',
    packages=['labelops'],
    install_requires=requirements,
)
