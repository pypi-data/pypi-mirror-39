#!/usr/bin/env python3
import sys

import setuptools

def main():
	if sys.version_info[:2] < (3, 5):
		raise SystemExit("conflictify requires at least Python 3.5.")
	setuptools.setup(
		name="conflictify",
		version="1.0.0",
		description="A Python module for identifying which files have merge conflicts between two branches in a Git checkout.",
		url="https://gitlab.com/chrisgavin/conflictify/",
		packages=["conflictify"],
		python_requires=">=3.5",
		classifiers=[
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3 :: Only",
		],
		extras_require={
			"dev": [
				"pytest",
				"mypy",
			]
		},
	)

if __name__ == "__main__":
	main()
