# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in jude_customization/__init__.py
from jude_customization import __version__ as version

setup(
	name='jude_customization',
	version=version,
	description='Custom utilities',
	author='Anthony Emmanuel, github.com/mymi14ss',
	author_email='mymi14s@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
