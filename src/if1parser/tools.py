# tools.py
# Mathijs Saey
# dvm prototype

""" 
This module contains a few tools for parser creation
"""

import sys

def warning(msg, line = "?"):
	print "Warning\t at line:", line, "\t:", msg

def error(msg, line = "?"):
	print "Error\t at line:", line, "\t:", msg
	sys.exit()