# encoding: utf-8

from __future__ import unicode_literals, print_function

from functools import partial

from marrow.package.host import PluginManager


def collect(self, pretend=False, pretend=False, plugins=None: partial(str.split, sep=',')):
	"""Collect static resources.
	
	Most applications serve static files from the development server, in production, however, you'll want a high-
	performance web server doing this.
	
	This command gathers static resources from your applciation and any other applications you have embedded and
	emits them with optional minification.
	"""
	
	for collector in PluginManager('web.collect', plugins):
		collector(cli, pretend=pretend)
