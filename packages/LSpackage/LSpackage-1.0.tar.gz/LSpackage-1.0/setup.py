#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from distutils.core import setup

setup(
    name='LSpackage',
    version='1.0',
    description=u'An implementation of Local Search algorithms based on single solution design',
    long_description=open('README.rst').read(),
    author=u'Andurnache Alexandru',
    author_email='alex.andur@yahoo.com',
    url='http://github.com/alexandur/LSpackage',
    packages=['code'],
    license='LICENSE.txt',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
