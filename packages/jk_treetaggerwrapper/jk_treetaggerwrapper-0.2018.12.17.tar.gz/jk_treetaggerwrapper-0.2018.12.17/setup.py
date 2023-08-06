from setuptools import setup


def readme():
	with open("README.rst") as f:
		return f.read()


setup(name = "jk_treetaggerwrapper",
	version = "0.2018.12.17",
	description = "This python module provides a wrapper around treetagger.",
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	license = "Apache 2.0",
	url = "https://github.com/jkpubsrc/python-module-jk-treetaggerwrapper",
	download_url = "https://github.com/jkpubsrc/python-module-jk-treetaggerwrapper/tarball/0.2018.12.17",
	keywords = [
		"treetagger",
		"pos-tagging"
	],
	packages = [
		"jk_treetaggerwrapper",
	],
	install_requires = [
		"treetaggerwrapper",
		#"jk_utils",
	],
	include_package_data = True,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 3.5",
		"License :: OSI Approved :: Apache Software License"
	],
	long_description = readme(),
	zip_safe = False)












