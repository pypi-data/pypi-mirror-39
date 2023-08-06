#!/usr/bin/env python

from setuptools import setup, find_packages

# http://bit.ly/2alyerp
with open('utf_remote/_version.py') as f:
    exec(f.read())

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='utf_remote',
    version=__version__,
    description="Platform for connected devices",
    long_description=long_desc,
    author='Shayan Ahmed',
    author_email='shayanahmed46@yahoo.com',
    platforms=['any'],
    packages=find_packages(),

    entry_points={
        "console_scripts": [
           'utf_remote = utf_remote.app:main'
        ]
    },

    install_requires=[
        'enum34==1.1.6',
        'six==1.10.0',
        'ws4py==0.3.5',
    ],

    zip_safe=True
)
