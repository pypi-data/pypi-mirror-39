#!/usr/env/bin python
#-*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xmind-sdk-python-upload-file",
    version="1.0",
    author="qinglin",
    author_email="1148865821@qq.com",
    description="The offical XMind python SDK",
    long_description=long_description,
    
    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    license="MIT",
    keywords="XMind, SDK, mind mapping",
    python_requires='>=3.6',

    url="https://github.com/xqlip/xmind-sdk-python.git",
    download_url='https://github.com/xqlip/xmind-sdk-python/archive/v1.1.tar.gz',
)
