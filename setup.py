#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='dotcon',
    packages=['dotcon'],
    version='0.0.1',
    description='Dotfile configuration management made easy',
    author='David Deprost',
    author_email='dadeprost@gmail.com',
    install_requires=[], # toml
    entry_points = {
        'console_scripts': [
            'dotcon = dotcon.dotcon:main',
        ],
    },
)