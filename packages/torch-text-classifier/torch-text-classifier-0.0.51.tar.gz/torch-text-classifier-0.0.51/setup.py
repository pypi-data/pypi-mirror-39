#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: InfinityFuture
# Mail: infinityfuture@foxmail.com
# Created Time: 2018-09-06 10:00:00
#############################################

import os
from setuptools import setup, find_packages

ON_RTD = os.environ.get('READTHEDOCS') == 'True'
if not ON_RTD:
    INSTALL_REQUIRES = [
        'torch', 'tqdm', 'scikit-learn', 'numpy', 'scipy', 'pypinyin'
    ]
else:
    INSTALL_REQUIRES = []

VERSION = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    'version.txt'
)

setup(
    name='torch-text-classifier',
    version=open(VERSION, 'r').read().strip(),
    keywords=('pip', 'pytorch', 'classifier'),
    description='NLP tool',
    long_description='NLP tool, text classifier',
    license='MIT Licence',
    url='https://github.com/infinity-future/torch-text-classifier',
    author='infinityfuture',
    author_email='infinityfuture@foxmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=INSTALL_REQUIRES
)
