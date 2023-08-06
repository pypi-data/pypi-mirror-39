#!/usr/bin env python3
# coding: utf-8
from setuptools import setup

setup(
    name='lblemcli',
    version='0.1',
    author='libinglin',
    author_email='libinglin@126.com',
    url='https://github.com',
    description='A email client in terminal',
    packages=['emcli'],
    install_requires=['yagmail'],
    tests_require=['nose', 'tox'],
    entry_points={'console_scripts': ['lblemcli=emcli:main']}
)
