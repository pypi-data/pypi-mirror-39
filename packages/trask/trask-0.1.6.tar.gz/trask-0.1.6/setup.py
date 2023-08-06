# pylint: disable=missing-docstring

import setuptools

setuptools.setup(
    name='trask',
    version='0.1.6',
    description='Declarative recipe-based task runner',
    url='https://github.com/nicholasbishop/trask',
    author='Nicholas Bishop',
    author_email='nicholasbishop@gmail.com',
    py_modules=['trask'],
    install_requires=['attrs', 'tatsu'])
