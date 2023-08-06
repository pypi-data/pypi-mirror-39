#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Caffe SSD for windows
"""
import platform
from setuptools import setup

setup(
    name = 'caffe-ssd-x86',
    version = '1.0.0.0',
    packages = [
        'caffe',
    ],
    install_requires=[
        'numpy',
        'opencv-python',
        'protobuf',
        'scikit-image',
        'scipy',
    ],
    license = 'Apache License',
    author = 'Baidu',
    author_email = 'aipe@baidu.com',
    url = 'https://github.com/Baidu-AIP',
    description = 'Baidu Caffe SSD For Windows',
    keywords = [ 'caffe', 'caff-ssd', 'windows',]
)
