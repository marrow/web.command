#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
	raise SystemExit("Python 3.2 or later is required.")

exec(open(os.path.join("web", "command", "release.py")).read())


class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-spec',  # output formatting
	]


setup(
	name = "web.command",
	version = version,
	
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	download_url = 'https://github.com/marrow/web.command/releases',
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = [
			'WebCore',  # This package is meant to interoperate with the WebCore framework.
			'cli',
			'command',
		],
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
		],
	
	packages = find_packages(exclude=['documentation', 'example', 'test']),
	include_package_data = True,
	namespace_packages = [
			'web',  # primary namespace
			'web.command',  # extensible command-line interface and scripts
		],
	
	entry_points = {
			# Python Standard
			'console_scripts': ['web = web.__main__:main'],  # extensible command line interface
			'gui_scripts': [],  # for future use, i.e. "native" applications
			
			# Command-line scripts for administrative purposes.
			'web.command': [
					# report versions, explore plugins, and identify updates
					'versions = web.command.versions:versions',
					
					# scrub your project of caches
					'clean = web.command.clean:clean',
					
					# collect static resources for deployment
					'collect = web.command.collect:collect',
					
					# pre-populate your project's caches
					'compile = web.command.compile:compile',
					
					# serve your project on the web
					'serve = web.command.serve:serve',
					
					# start an interactive REPL shell
					'shell = web.command.shell:shell',
				],
			
			'web.clean': [
					# compiled Python bytecode
					'python = web.command.clean:clean_python',
				],
			
			'web.collect': [
				],
			
			'web.compile': [
					# Python bytecode compilation
					'python = web.command.compile:compile_python',
				],
			},
	
	install_requires = [
			'marrow.package<2.0',  # dynamic execution and plugin management
			'pyyaml',  # rich data interchange format; used for configuration
		],
	
	extras_require = dict(
			development = tests_require,
		),
	
	tests_require = tests_require,
	
	zip_safe = True,
	cmdclass = dict(
			test = PyTest,
		)
)
