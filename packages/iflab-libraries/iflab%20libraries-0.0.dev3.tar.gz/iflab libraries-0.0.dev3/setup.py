#!/usr/bin/env python
# -*- coding:utf-8 -*-

#refer to
#https://qiita.com/icoxfog417/items/edba14600323df6bf5e0
#https://qiita.com/kinpira/items/0a4e7c78fc5dd28bd695

from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

def _read_readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        return ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '') for line in open(os.path.join(here, 'iflb', '__init__.py')) if line.startswith('__version__ = ')), '0.0.dev3')

setup(
    name="iflab libraries"
    , version=version
    , url='https://github.com/user/iflb'
    , author='teppei@iflab.tokyo'
    , author_email='teppei@iflab.tokyo'
    , maintainer='teppei'
    , maintainer_email='teppei@iflab.tokyo'
    , description='Iflab common libraries'
    , long_description=_read_readme()
    #, long_description_content_type="text/markdown"
    #, packages=find_packages()
    , packages=['iflb']
    #, install_requires=_requires_from_file('requirements.txt')
    , license="MIT"
    , classifiers=[
        "Programming Language :: Python :: 3"
        , "License :: OSI Approved :: MIT License"
        , "Operating System :: OS Independent"
    ]
    , entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    pkgdep = iflb.scripts.command:main
    """,
)
