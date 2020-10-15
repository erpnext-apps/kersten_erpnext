# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in kersten_erpnext/__init__.py
from kersten_erpnext import __version__ as version

setup(
	name='kersten_erpnext',
	version=version,
	description='Custom App for building item web pages from page builder',
	author='frappe',
	author_email='hello@frappe.io',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
