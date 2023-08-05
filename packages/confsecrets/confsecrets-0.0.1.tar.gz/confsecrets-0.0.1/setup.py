#!/usr/bin/env python
import os
import subprocess

from setuptools import setup, find_packages


def get_version():
    """
    Determine a version string using git or a file VERSION.txt
    """
    # VERSION.txt is not added to git, it can be generated manually or by CI/CD
    version = '0.0.1'
    if os.path.isfile('VERSION.txt'):
        with open('VERSION.txt', 'r') as f:
            version = f.read().strip()
    return version


def get_readme():
    """
    Open and read the readme. This would be the place to convert to RST, but we no longer have to.
    """
    with open('README.md') as f:
        return f.read()


setup(
    name='confsecrets',
    version=get_version(),
    description='Simple utility to symmetrically encrypt/decrypt application secrets',
    long_description=get_readme(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=CommonMark',
    author='Dan Davis',
    author_email='dan@danizen.net',
    maintainer='Dan Davis',
    maintainer_email='dan@danizen.net',
    url='https://github.com/danizen/confsecrets.git',
    project_urls={
        'Documentation': 'https://danizen.github.io/confsecrets/',
    },
    packages=[
        'confsecrets',
        'djsecrets',
    ],
    #entry_points={
    #    'console_scripts': [
    #        'confsecrets=confsecrets.cli:main',
    #    ]
    #},
    tests_require=['pytest', 'pytest-cov', 'flake8', 'Django>1.11,<2', 'coverage', 'tox', 'PyCrypto', 'six'],
    install_requires=['PyCrypto', 'six'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)

