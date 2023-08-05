#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='Codemao-AI',
    version='0.0.1',
    description=(
        'A Python library created by Codemao.Inc for Python-learners to do something cool!"'
    ),
    long_description=open('README.rst').read(),
    query='Codemao',
    author='Codemao',
    author_email='wood@codemao.cn',
    maintainer='Codemao',
    maintainer_email='wood@codemao.cn',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://python.codemao.cn',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)

