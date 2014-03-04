# __init__.py
# Mathijs Saey
# DISc

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
# \package IF1
# \author Mathijs Saey
# 
# \brief DISc IF1 Parser.
#
# This module parses [IF1](\ref IF1) files and converts them to IGR.
##

import type
import edge
import graph

import logging
log = logging.getLogger(__name__)

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
	'{' : graph.parseCompoundStart,
	'}' : graph.parseCompoundEnd
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
		log.warning("Line %d, Unrecognized line type: %s", ctr, key)
	except Exception, e:
		log.error("Line %d, Exception %s while parsing: '%s'". ctr, e, line)
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
def fromString(str):
	ctr = 1
	lines = str.split("\n")
	for line in lines:
		if len(line) is not 0:
			parseLine(line, ctr)
			ctr += 1
