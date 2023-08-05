#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/7 上午11:47

import re
import setuptools

with open('README.md', 'r') as f:
    long_desc = f.read()

with open('nbase/__init__.py', 'r') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name='Nbase',
    version=version,
    author='Ding Weihua',
    author_email='weihua.ding@nio.com',
    description='A simple toolkit for Nio UDP team.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Flask',
        'pytz',
        'pymongo',
        'pandas',
        'redis',
        'redis-py-cluster',
        'kafka',
        'elasticsearch',
        'boto3',
    ]
)
