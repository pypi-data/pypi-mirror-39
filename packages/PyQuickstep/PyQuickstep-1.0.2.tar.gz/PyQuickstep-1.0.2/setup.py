#!/usr/bin/env python
import io
from setuptools import setup, find_packages

version = "1.0.2"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyQuickstep",
    version=version,
    url='https://github.com/raghu1994/PyQuickstep',
    description='Pure Python MySQL Driver',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'cryptography', 'google', 'protobuf', 'grpcio', 'grpcio-tools'
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    keywords="Quickstep",
)