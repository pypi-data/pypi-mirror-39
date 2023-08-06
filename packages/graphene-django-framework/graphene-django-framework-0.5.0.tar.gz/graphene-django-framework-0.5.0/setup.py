#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

from graphene_django_framework import __version__

try:
    from pypandoc import convert_file as convert
except ImportError:
    import io

    def convert(filename, fmt):
        with io.open(filename, encoding='utf-8') as fd:
            return fd.read()

DESCRIPTION = 'A framework for using GraphQL with Django.'

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(
    name='graphene-django-framework',
    version=__version__,
    author='Kevin Clark',
    # author_email='kevin@example.com',
    description=DESCRIPTION,
    long_description=convert('README.md', 'rst'),
    url='https://gitlab.com/hybridlogic/graphene-django-framework/',
    license='Apache Software License',
    keywords=['django','graphene', 'graphql', 'relay'],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['server', 'docs']),
    include_package_data=True,
)
