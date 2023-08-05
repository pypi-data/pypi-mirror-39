#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: setup.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2017
from setuptools import setup


setup(
    name='chance-exception-capturer',
    version='0.0.2',
    description='The exception capturer for chancefocus',
    url='https://gitee.com/QianFuFinancial/chance-exception-capturer.git',
    author='Jimin Huang',
    author_email='huangjimin@whu.edu.cn',
    license='MIT',
    packages=['exception_capturer'],
    install_requires=[
        'nose>=1.3.7',
        'coverage>=4.1',
    ],
    zip_safe=False,
)
