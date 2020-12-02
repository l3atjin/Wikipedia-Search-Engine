"""
Index server python package configuration.

Nilay Muchhala  <nilaym@umich.edu>
Aneeqa Fatima   <aneeqaf@umich.edu>
"""

from setuptools import setup

setup(
    name='index',
    version='0.1.0',
    packages=['index'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
    ],
    python_requires='>=3.6',
)
