#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

from even_tester import __version__, __mod_name__


try:
    with open("README.md", 'r') as f:
        long_description = f.read()
    with open('requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f.readlines()]
except:
    long_description='A python-cpp even_tester by srb',
    requirements = []

try:
    from even_tester.installer import install_tester
    install_tester()
except:
    print('something bad happened')

setup(
    name=__mod_name__,
    version=__version__,
    description='A python library by srb',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sarbjit Singh',
    author_email='srbcheema2@gmail.com',
    url='http://github.com/srbcheema2/'+__mod_name__,

    packages=find_packages(), # provides same list, looks for __init__.py file in dir
    include_package_data=True,
    install_requires=requirements, #external packages as dependencies

    entry_points={
        'console_scripts': [__mod_name__+'='+__mod_name__+'.main:main']
    },

    classifiers=[
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    license='MIT License',
)
