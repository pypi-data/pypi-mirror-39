#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='zevcrack',
    version='0.0.2',
    description='Advanced hash cracker',
    author='noval wahyu ramadhan',
    author_email='xnver404@gmail.com',
    url='https://github.com/zevtyardt/zevcrack',
    py_modules = ['zevcrack'],
    include_package_data=True,
    install_requires=[
        'passlib',
        'requests'
    ],
    license="MIT",
    zip_safe=False,
    keywords='zevcrack',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={'console_scripts': ['zevcrack = zevcrack:main']},
)
