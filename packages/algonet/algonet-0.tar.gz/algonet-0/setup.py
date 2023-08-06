#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgoNet.

"""

__author__ = "Felix Petersen"
__email__ = "mail@felix-petersen.de"

import setuptools

import algonet

setuptools.setup(
    description='AlgoNet - algorithmic neural networks',
    author='Felix Petersen',
    author_email='mail@felix-petersen.de',
    url='https://github.com/Felix-Petersen/AlgoNet.git',
    license='GPLv3 License',
    version=algonet.__version__,
    name='algonet',
    packages=['algonet'],
    install_requires=['numpy', 'torch'],
)