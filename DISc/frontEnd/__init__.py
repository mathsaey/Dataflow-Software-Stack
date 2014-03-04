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
# \package frontend
# \brief DISc Frontend Selector
# 
# This module serves as an interface to any frontend that the user may choose.
# Any frontEnd module should define a fromString function that is reachable from
# it's package. (defined in the __init__ file of this package).
##

import importlib

import logging
log = logging.getLogger(__name__)

frontEnd = None

##
# Select a frontend to use.
#
# \param name 
#		A name that matches a package in the
#		frontEnd package.
##
def set(name):
	global frontEnd
	try:
		frontEnd = importlib.import_module('.%s' % name, __name__)
	except ImportError:
		log.error("Frontend '%s' not found.", name)

##
# Convert the given string to IGR.
# This simply calls the same method on
# the selected frontend.
#
# \param str
#		The string to convert to IGR.
##
def fromString(str):
	if frontEnd:
		frontEnd.fromString(str)
	else:
		log.error("No frontEnd specified...")

##
# Convert the contents of a file to
# IGR. This simply calls fromString()
# on the contents of the file.
#
# \param path
#		The path of the file.
##
def fromFile(path):
	file = open(path, 'r')
	fromString(file.read())