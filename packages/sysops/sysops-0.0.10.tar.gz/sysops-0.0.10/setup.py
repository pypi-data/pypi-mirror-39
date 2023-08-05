#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='sysops',
    version='0.0.10',
    description='just for test',
    classifiers=[
        # 'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        # 'Intended Audience :: Developers',
        # 'Operating System :: OS Independent',
    ],
    author='xxy1991',
    # url='https://github.com',
    # author_email='xxy1991@gmail.com',
    # license='MIT',
    install_requires=['invoke>=1.2'],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=False,
    zip_safe=True,
)
