# parser.py
# Mathijs Saey
# dvm

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

##
# \file parser.py
# \namespace if1parser.parser
# \brief Main parser loop
# 
# This module is the main parser interface.
# It is responsible for scanning the type of the IF1
# instructions and calling the correct module for this type. 
##

import type
import edge
import graph
import tools

# ------ #
# Parser #
# ------ #

## Skip a line #
def skipLine(str, ctr): pass

##
# Parser values and the function to call when
# they are encountered
##
__FUNCTIONS__ = {
	'C' : skipLine,
	'T' : type.parseType,
	'E' : edge.parseEdge,
	'L' : edge.parseLiteral,
	'N' : graph.parseNode,
	'G' : graph.parseGraph,
	'X' : graph.parseGraph,
	'{' : skipLine,
	'}' : skipLine
}

##
# Parse a single if1 line.
#
# \param line
#		The string of the line to parse
# \param ctr
#		The line number of the current line,
#		used for error handling.
##
def parseLine(line, ctr = "?"):
	arr = line.split()
	key = line[0]
	try:
		func = __FUNCTIONS__[key]
	except KeyError:
		warn = "Unrecognized line type: " + key
		tools.warning(warn, ctr)
	except Exception, e:
		error = "Exception: '" + str(e) + "' while parsing: '" + line + "'"
		tools.error(error, ctr)
	else:
		func(arr, ctr)

##
# Parse a complete IF1 string.
# This function simply splits the file 
# based on the newlines and passes each
# line to parseLine()
#
# \param str
#		The string
##
def parseString(str):
	ctr = 1
	lines = str.split("\n")
	for line in lines:
		if len(line) is not 0:
			parseLine(line, ctr)
			ctr += 1

##
# Parses an IF1 file.
# Simply extracts the contents of the
# file before passing it to parseString()
#
# \param loc
#		The location of the file.
##
def parseFile(loc):
	file = open(loc, 'r')
	parseString(file.read())