#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from distutils.core import setup

setup(
    name = 'LSpackage',
    version = '0.1',
    description = 'An implementation of Local Search algorithms based on single solution design',
    long_description = open('README.rst').read(),
    author = 'Andurnache Alexandru',
    author_email = 'alex.andur@yahoo.com',
    url = 'http://github.com/alexandur/LSpackage',
    packages = ['code'],
    license = 'LICENSE.txt',
classifiers = [
	"Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
    ],
    
    
)
