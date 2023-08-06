# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='kutils',
    version='0.3.0',
    description="Kyle's utilities",
    long_description=readme,
    author='K. Isom',
    author_email='kyle@imap.cc',
    url='https://github.com/kisom/pykutils',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
