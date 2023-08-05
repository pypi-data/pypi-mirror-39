#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit deepdata_alpha/__version__.py
version = {}
with open(os.path.join(here, 'deepdata_alpha', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='deepdata_alpha',
    version=version['__version__'],
    description="The package is for developing algorithm in prediction.",
    long_description=readme + '\n\n',
    author="John J. H. Lin",
    author_email='john.jrhunglin@gmail.com',
    url='https://github.com/John/deepdata_alpha',
    packages=[
        'deepdata_alpha',
    ],
    package_dir={'deepdata_alpha':
                 'deepdata_alpha'},
    include_package_data=True,
    zip_safe=False,
    keywords='deepdata_alpha',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    install_requires=[],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
