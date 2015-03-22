# encoding: utf-8

"""Interactive execution beautifiers.

Most definitely not intended for multiplexed (multithreaded) use.
"""

# Inspiration from: /lib/gentoo/functions.sh /lib64/rc/sh/functions.sh

import sys
from contextlib import contextmanager


TTY = sys.stdout.is_tty()

QUIET = False
DEBUG = False  # Display exception tracebacks.
COLOR = 'auto'

BULLET_TEMPLATE = ' {level}*{clear} '
INDENT = '   '
STACK = []


# namedtuple('Point', ['x', 'y'])



partial = False
partial_position = None


@contextmanager
def indent():
	"""Increase the global scope, causes logging messages to be indented."""
	
	global indent_level
	indent_level += 1
	yield
	indent_level -= 1


@contextmanager
def estatus(status, message, newline=True):
	global partial
	
	if not newline:
		partial = True
	
	
	
	try:
		yield
	
	except:
		pass
	
	else:
		pass
	
	partial = False


@contextmanager
def einfo(message, newline=True):
	with estatus('info', message, newline):
		yield


def ewarn(newline=True):
	with estatus('info', message, newline):
		yield


@contextmanager
def einfo(newline=True):
	with estatus('info', message, newline):
		yield


@contextmanager
def einfo(newline=True):
	with estatus('info', message, newline):
		yield



