''' Installer for the package. '''

import pathlib
from setuptools import find_packages, setup

PATH = pathlib.Path(__file__).parent

README = (PATH / "README.md").read_text()

setup(
	name = 'oven',
	version = '0.1.0',
	description = 'An util package that includes features from other languages\' stdlib.',
	long_description = README,
	long_description_content_type = "text/markdown",
	url = 'https://github.com/davidmaamoaix/Oven',
	author = 'David Ma',
	author_email = "davidma@davidma.cn",
	license = 'MIT',
	packages = find_packages(),
	include_package_data = True,
)