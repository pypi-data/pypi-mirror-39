#!/usr/local/bin/python3

import argparse
import os
import platform
import re
import shutil
import subprocess
import traceback
from pathlib import PurePath

from builtins import FileNotFoundError
from typing import Dict, List


class Dependency:
	CONDITION_RE = re.compile('^(\+.+)\:')

	class Type:
		PYPI = 'pypi'
		LOCAL = 'local'
		VCS = 'vcs'

	def __init__(self, dtype: str, condition: set, name: str, path: str):
		self.dtype = dtype
		self.condition = condition
		self.name = name
		self.path = path

	@classmethod
	def parse(cls, line: str):
		match = cls.CONDITION_RE.match(line)

		dep = line
		condition = set()
		if match:
			condition = set(match.group(1).lstrip("+").split("+"))
			p = match.span(0)[1]
			dep = line[p:]

		dep_name = dep
		path = dep

		dtype = cls.Type.PYPI

		if "==" in dep:
			dep_parts = dep.split("==")
			dep_name = dep_parts[0]

			if "://" in dep_parts[1]:
				path = dep_parts[1]
				dtype = cls.Type.VCS

			elif "/" in dep_parts[1]:
				path = dep_parts[1]
				dtype = cls.Type.LOCAL

		elif "/" in dep:
			# Normalize path to strip last fs separators and get base name
			dep_name = os.path.basename(os.path.normpath(dep))
			dtype = cls.Type.LOCAL

		return Dependency(dtype, condition, dep_name, path)

	def __eq__(self, other):
		return self.dtype == other.dtype and self.condition == other.condition and self.name == other.name and self.path == other.path

	def __repr__(self):
		return "Dependency(%s, %s, %s, %s)" % ('Dependency.Type.' + self.dtype.upper(), repr(self.condition), repr(self.name), repr(self.path))


class Rules:
	def __init__(self):
		self.default: Dependency = None
		self.rules: List[Dependency] = []


class Env:
	def __init__(self, stream):
		self.venv_path: str = 'venv'

		self.deps: Dict[str, Rules] = {}

		for line in stream:
			line = line.strip()
			if not line:
				continue

			dep = Dependency.parse(line)

			self.deps.setdefault(dep.name, Rules())

			if dep.condition:
				self.deps[dep.name].rules.append(dep)
			else:
				self.deps[dep.name].default = dep


class Executor:
	VERSION_RE = re.compile('^Version: (.+)$')

	def __init__(self):
		self.venv_path = None

	def _python(self):
		if platform.system() == "Windows":
			return os.path.join(self.venv_path, "Scripts", "Python.exe")
		else:
			return os.path.join(self.venv_path, "bin", "python")

	def _pip(self):
		if platform.system() == "Windows":
			return os.path.join(self.venv_path, "Scripts", "Pip.exe")
		else:
			return os.path.join(self.venv_path, "bin", "pip")

	def _find_setup_py(self, path: str):
		root_path = PurePath(path).root
		install_path = os.path.abspath(path)
		for path_it in range(10):
			if install_path == root_path:
				break
			if os.path.exists(os.path.join(install_path, "setup.py")):
				return install_path
			install_path = os.path.dirname(install_path)

		return None

	def run(self, args: argparse.Namespace, dummy: bool=False):
		filename = args.filename
		flags = set(flag.lstrip('+') for flag in args.flags)

		try:
			env = Env(open(filename))
		except FileNotFoundError:
			print("File '%s' not found" % filename)
			exit(-1)
			return  # Suppress PyCharm inspection

		self.venv_path = env.venv_path

		if not os.path.exists(self.venv_path) or not os.path.exists(self._pip()):
			if not dummy:
				if os.path.exists(self.venv_path):
					shutil.rmtree(self.venv_path)

				print("Creating venv...")
				subprocess.check_call(["python3", "-m", "venv", self.venv_path])
				subprocess.check_call([self._python(), "-m", "pip", "install", "--upgrade", "pip"])

		pypi_install_list = []
		for dep_name, rules in env.deps.items():
			execute = None

			if flags:
				for rule in rules.rules:
					if rule.condition & flags:
						if execute is not None:
							raise ValueError("Ambigious!")
						execute = rule

			if not execute:
				execute = rules.default

			if execute and not dummy:
				local_dst_exists = False
				local_dst = execute.name
				if execute.dtype == Dependency.Type.LOCAL:
					setup_py_path = self._find_setup_py(execute.path)
					if setup_py_path:
						print("Installing %s deps..." % execute.name)
						subprocess.check_call([self._pip(), "install", setup_py_path])
						subprocess.check_call([self._pip(), "uninstall", execute.name, "--yes"])

					if os.path.islink(local_dst):
						if os.path.realpath(local_dst) == execute.path:
							# Ensure actual execute path
							local_dst_exists = True
						else:
							print("Remove symlink %s to %s" % (local_dst, os.path.realpath(local_dst)))
							os.remove(local_dst)
				else:
					if os.path.islink(local_dst):
						print("Remove symlink %s to %s" % (local_dst, os.path.realpath(local_dst)))
						os.remove(local_dst)
					else:
						local_dst_exists = True

				if execute.dtype == Dependency.Type.LOCAL:
					subprocess.check_call([self._pip(), "uninstall", execute.name, "--yes"])
					if not local_dst_exists:
						print("Symlink %s to %s" % (execute.path, local_dst))
						os.symlink(execute.path, local_dst)
				elif execute.dtype == Dependency.Type.PYPI:
					pypi_install_list.append(execute.path)

				elif execute.dtype == Dependency.Type.VCS:
					subprocess.check_call([self._pip(), "install", execute.path, "--upgrade", "--force-reinstall"])
					# FIXME: correct replace
					# self._rewrite_version(execute, filename)

		if pypi_install_list:
			cmd = [self._pip(), "install"] + pypi_install_list
			if args.index_url:
				cmd += ["-i", args.index_url]
			subprocess.check_call(cmd)

	def _get_package_version(self, dep_name: str):
		out = subprocess.check_output([self._pip(), "show", dep_name])
		info = out.decode("utf-8").split("\n")
		for line in info:
			m = self.VERSION_RE.match(line)
			if m:
				return m[1]

		raise RuntimeError("Can't find version")

	def _rewrite_version_content(self, content: str, rule: Dependency, version: str):
		p = re.compile('(?:\s+|^)(%s)(?:\s+|$|\=)' % rule.name)
		# new_content = content.replace(rule.name, rule.name + "==" + version)
		new_content = p.sub(rule.name + "==" + version, content)
		return new_content

	def _rewrite_version(self, rule: Dependency, filename: str, get_package_version_func=None):
		if get_package_version_func is None:
			get_package_version_func = self._get_package_version

		try:
			if rule.dtype != rule.Type.LOCAL:
				version = get_package_version_func(rule.name)
				with open(filename) as f:
					content = f.read()

				new_content = self._rewrite_version_content(content, rule, version)

				with open(filename, "w") as f:
					f.write(new_content)
		except:
			print(traceback.format_exc())


__version__ = "0.4"


def main():
	executor = Executor()

	parser = argparse.ArgumentParser(description="qiq thin layer over pip with a few principles.")
	parser.add_argument("-v", "--version", action="version", version="qiq " + __version__)
	parser.add_argument("flags", metavar="FLAGS", type=str, nargs="*", help="flags")
	parser.add_argument("-f", "--filename", type=str, default="qiq.txt", help="qiq input file")
	parser.add_argument("-i", "--index-url", type=str, default=None, help="pip index url")
	args = parser.parse_args()

	executor.run(args)


if __name__ == "__main__":
	main()
