"""
Search server python package configuration.

Nilay Muchhala  <nilaym@umich.edu>
Aneeqa Fatima   <aneeqaf@umich.edu>
"""

from setuptools import setup

setup(
    name='search',
    version='0.1.0',
    packages=['search'],
    include_package_data=True,
    install_requires=[
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
    ],
    python_requires='>=3.6',
)
