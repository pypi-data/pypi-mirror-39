#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def version():
    git_version = None
    try:
        git_tag = subprocess.check_output(['git', 'describe', '--tags'])
        if git_tag:
            git_version = git_tag.strip()[1:].decode('utf-8')
    except:
        pass
    if not git_version:
        git_version = 'SNAPSHOT'
    return git_version


setup(
    name='marshmallow-dynamodb',
    version=version(),
    packages=['marshmallow_dynamodb'],
    description='Extra fields to integrate Marshmallow and DynamoDb',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Leonardo Santos Monteiro',
    author_email='leonardo.monteiro@truckpad.com.br',
    url='https://github.com/truckpad/marshmallow-dynamodb',
    install_requires=read('requirements.txt').strip().split('\n'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
