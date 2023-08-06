#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='tdexApi',
    version='1.1.1',
    description=(
        'tdex api'
    ),
    author='lamsam',
    author_email='sam_yulam@163.com',
    maintainer='lamsam',
    maintainer_email='sam_yulam@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/tdex-exchange',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
