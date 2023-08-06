#!/usr/bin/env python

import os.path as op

from setuptools import setup, find_packages


basedir = op.dirname(__file__)


with open('requirements.txt', 'rt') as f:
    install_requires = [line.strip() for line in f.readlines()]
    install_requires = [line for line in install_requires if line != '']


version = {}
with open(op.join(basedir, 'ukbparse', '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__ = '):
            exec(line, version)
            break
version = version['__version__']


with open(op.join(basedir, 'README.rst'), 'rt') as f:
    readme = f.read()


setup(
    name='ukbparse',
    version=version,
    description='UK Biobank data processing library',
    long_description=readme,
    url='https://git.fmrib.ox.ac.uk/fsl/ukbparse',
    author='Paul McCarthy',
    author_email='pauldmccarthy@gmail.com',
    license='Apache License Version 2.0',

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts' : [
            'ukbparse = ukbparse.main:main',
        ]
    }
)
