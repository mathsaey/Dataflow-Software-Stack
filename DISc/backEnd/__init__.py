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
# \package backEnd
# \brief DISc backend Selector
# 
# This module serves as an interface to any backend that the user may choose.
#
# A backend only needs to define 2 elements.
# * A function generate(), that takes no inputs and that 
#	returns a string version of the output language.
# * An *extension* attribute that contains the file extension of the output language.
##

import importlib

import logging
log = logging.getLogger(__name__)

## Store the current back end
backEnd = None

## Path to the output file.
path = None

##
# Select a backend to use.
#
# \param name 
#		A name that matches a package in the
#		backend package.
##
def set(name):
	global backEnd
	try:
		backEnd = importlib.import_module('.%s' % name, __name__)
	except ImportError:
		log.error("Backend '%s' not found.", name)

##
# Set up the backend from the
# command line arguments.
#
# \param fileName
#		The name of the input file, without
#		the extension.
# \param backEndFlag
#		The value passed to the backend flag.
# \param outputFlag
#		The value passed to the output flag.
##
def setUp(fileName, backEndFlag, outputFlag):
	global path
	set(backEndFlag)

	if backEnd:
		if outputFlag: path = outputFlag
		else: path = '%s.%s' % (fileName, backEnd.extension)
	else:
		log.error("No backend specified...")

## 
# Ask the backend to
# Generate the output language.
##
def generate():
	if backEnd:
		return backEnd.generate()
	else:
		log.error("No backend specified...")

##
# Write the generated output
# to a file.
##
def toFile():
	if backEnd:
		result = generate()
		file = open(path, 'w')
		file.write(result)
		file.close()
	else:
		log.error("No backend specified...")
