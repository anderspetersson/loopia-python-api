#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='loopia',
    version='0.1.0',
    author='Anders Petersson',
    author_email='me@anderspetersson.se',
    url='http://github.com/anderspetersson/loopia-python-api',
    description='Loopia Python API',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
