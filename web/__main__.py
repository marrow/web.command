#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
import select
import logging
import pkg_resources

from marrow.script import describe
from marrow.script.core import ExitException

from web.command import release


__all__ = ['ScriptCore']


class ScriptCore(object):
	"""Extensible command line script dispatcher for the WebCore web framework."""
	
	_cmd_script = dict(
			title = "web",
			version = release.version,
			copyright = "Copyright 2012 Alice Bevan-McGregor and contributors"
		)
	
	@describe(
			verbose="Increase the default logging level to DEBUG.",
			quiet="Reduce the default logging level to WARN.",
			config="Specify a configuration file to use.",
			log="Where to send logging output; can use STDOUT and STDERR or the specifically named file.",
		)
	def __init__(self, verbose=False, quiet=False, config="local.yaml", log="STDERR"):
		self.verbose = verbose
		self.quiet = quiet
		self._config = config
		self.log = log
		
		levels = [logging.WARN, logging.INFO, logging.DEBUG]
		logging.basicConfig(level=levels[int(verbose)-int(quiet)+1])
	
	# Load plugins.
	locals().update({
			i.name: i.load()
			for i in pkg_resources.iter_entry_points('web.command')
		})
	
	def __getattr__(self, name):
		if not name.endswith('.yaml'):
			raise AttributeError("'ScriptCore' object has no attribute '"+name+"'")
		
		self._config = name


def main():
	from marrow.script import execute
	sys.exit(execute(ScriptCore))


if __name__ == '__main__':
	main()
