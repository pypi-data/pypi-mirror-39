#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import (
    setup,
    find_packages,
)

setup(
    name='xio',
    version='0.0.4',
    python_requires='>=3.5.*',
    description="""simple microframework for microservices rapid prototyping""",
    long_description=open('README.md').read(),
    author='Ludovic Jacquelin',
    author_email='ludovic.jacquelin@gmail.com',
    url='https://github.com/inxio/xio',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pyyaml",
        "pynacl",
        "ws4py",
        "ethereum;python_version<'3.0'",
        #"web3<4;python_version<'3.0'",
        "eth-typing<2;python_version>'3.0'",
        "web3>4.8;python_version>'3.0'",
    ],
    py_modules=['xio'],
    scripts=['bin/xio'],
    license="MIT",
    zip_safe=False,
    keywords='microframework microservices prototyping',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require={
        'server': [
            'gevent',
            'uswgi',
        ],
    },
)
