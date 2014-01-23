# parser.py
# Mathijs Saey
# dvm prototype

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

"""
This file serves as the top level access point for the parser.
"""

import type
import edge
import graph
import tools

# ------ #
# Parser #
# ------ #

def skipLine(str, ctr):
	pass

functions = {
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

def parseLine(line, ctr = "?"):
	arr = line.split()
	key = line[0]
	try:
		func = functions[key]
	except KeyError:
		error = "Unrecognized line type: " + key
		tools.error(error, ctr)
	except Exception, e:
		error = "Exception: '" + str(e) + "' while parsing: '" + line + "'"
		tools.error(error, ctr)
	else:
		func(arr, ctr)

def parseString(str):
	ctr = 1
	lines = str.split("\n")
	for line in lines:
		if len(line) is not 0:
			parseLine(line, ctr)
			ctr += 1

def parseFile(loc):
	file = open(loc, 'r')
	parseString(file.read())