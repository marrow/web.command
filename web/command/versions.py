# encoding: utf-8

from __future__ import print_function

import pkg_resources

from marrow.script import Parser
from marrow.script.util import wrap


E = "\033["
NO_COLOR = {'b': '', 'item': '', 'n': '', 'plug': '', 'pkg': '', 'ver': '', 'label': '', 'extra': '', 'extraf': ''}
COLOR = {'b': E+'1m', 'item': E+'1;32m', 'n': E+'0m', 'plug': E+'37;1m', 'pkg': E+'1;32m', 'ver': E+'33m', 'label': E+'32;2m', 'extra': E+'36m', 'extraf': E+'1;31m'}
C = COLOR

MD = ['Summary', 'Home-page', 'Author', 'Author-email', 'License']

def explore(namespace, short):
	for i in pkg_resources.iter_entry_points(namespace):
		if not short:
			metadata = dict(j.partition(': ')[::2] for j in i.dist._get_metadata(i.dist.PKG_INFO) if j.partition(':')[0] in MD)
			line = C['n'] + C['plug'] + i.name + C['n'] + " provided by " + C['pkg'] + \
					i.dist.project_name + " " + C['ver'] + i.dist.version + C['n']
			llen = len(line) - (3 + 3*len(C['n']) + len(C['item']) + len(C['plug']) + len(C['pkg']) + len(C['ver']))
			fail = []
			if i.extras:
				extras = []
				for extra in sorted(i.extras):
					if extra in i.dist._dep_map:  # It's an "extras_require".
						for dep in i.dist._dep_map[extra]:
							try:
								pkg_resources.require(str(dep))
							except pkg_resources.DistributionNotFound:
								fail.append(C['extraf'] + str(dep) + C['n'])
					if fail:
						extras.append(C['extraf'] + extra + C['n'] + " (missing: " + ", ".join(fail) + ")")
					else:
						extras.append(C['extra'] + extra + C['n'])
				print(" ", C['extraf'] if fail else C['item'], "* ", C['n'], line, C['extra'], C['b'], " + ", C['n'], ("\n "+C['extra']+C['b']+"+ "+C['n']).join(wrap(" ".join(extras), Parser.width() - llen).split("\n")), C['n'], sep='')
			else:
				print(" ", C['item'], "* ", C['n'], line, sep='')
			def md(label, line):
				labl = 12 - len(label)
				print("   ", C['label'], label, ":", labl * " ", C['n'], "\n   ".join(wrap(line, Parser.width() - (3+len(label)+2)).split("\n")), sep='')
			if 'Summary' in metadata: md('Description', metadata['Summary'])
			md("Location", i.dist.location)
			if 'Author' in metadata: md('Author', metadata['Author'] + ((' <' + metadata['Author-email'] + '>') if metadata.get('Author-email') else ''))
			if 'Home-page' in metadata: md('Homepage', metadata['Home-page'])
			if metadata.get('License'): md('License', metadata['License'])
		else:
			print("{0} ({1} {2})".format(i.name, i.dist.project_name, i.dist.version))
		print()


def dependencies(package, short):
	seen = dict()
	for i in pkg_resources.require(package):
		if i in seen: continue
		seen[i] = None
		
		if not short:
			print(" * {0} {1} from:".format(i.project_name, i.version))
			print("   ", "	 ".join(wrap(i.location, Parser.width() - 3).split("\n")), sep='', end="\n\n")
		else:
			print("{0} {1}".format(i.project_name, i.version))


def all_packages(short):
	seen = dict()
	for i in pkg_resources.working_set:
		if i in seen: continue
		seen[i] = None
		
		if not short:
			print(" * {0} {1} from:".format(i.project_name, i.version))
			print("   ", "	 ".join(wrap(i.location, Parser.width() - 3).split("\n")), sep='', end="\n\n")
		else:
			print("{0} {1}".format(i.project_name, i.version))


def all_namespaces():
	counts = dict()
	
	for i in pkg_resources.working_set:
		plugins = pkg_resources.get_entry_map(i)
		for k in plugins:
			counts.setdefault(k, 0)
			counts[k] += len(plugins[k])
	
	for k in sorted(counts):
		print(" * {0} ({1} plugins)".format(k, counts[k]))


def versions(self, all=False, package='WebCore', namespace=None, namespaces=False, short=False, color=True):
	"""Display versions of installed packages.
	
	Use the namespace argument to enumerate all plugins for the given namespace.  Examples include: console_scripts, web.command, web.db.engines, web.dispatch, marrow.templating, ...
	
	Example calls:
	
	web versions --all
	# dump all installed packages
	
	web versions --package mako
	# dump requirements for specific package
	
	web versions --namespaces
	# show available plugin namespaces
	
	web versions --namespace marrow.templating
	# show all plugins for this namespace
	
	web versions --short
	# one line per requirement, no paths or formatting
	"""
	
	global C
	
	# TODO: Determine if versions are latest, and if safe upgrading is possible.
	if color:
		C = COLOR
	else:
		C = NO_COLOR
	
	if namespace:
		print("Plugins within the \"{0}\" namespace:\n".format(namespace))
		return explore(namespace, short)
	
	if all:
		print("All installed Python packages:\n")
		return all_packages(short)
	
	if namespaces:
		print("Plugin namespaces:\n")
		return all_namespaces()
	
	print(package, "and dependencies:\n")
	return dependencies(package, short)
