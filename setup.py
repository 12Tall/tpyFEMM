# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tpyFEMM',
    version='0.1.0',
    description='Typed PyFEMM library',
    long_description=readme,
    author='Fubiao Ouyang',
    author_email='fb.ouyang@outlook.com',
    url='https://github.com/12tall/tpyFEMM',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
