#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name='cigopt',
    version='0.1',
    description='Like Sigopt, but free',
    packages=find_packages(exclude=['env', 'tests*', 'examples', 'ci', 'docs']),
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        'test': ['pytest==3.7.4', 'pytest-cov==2.5.1'],
        'docs': ['pydoc-markdown']
    },
    entry_points={},
    zip_safe=False,
)
