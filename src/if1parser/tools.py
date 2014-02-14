# tools.py
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
# \file if1parser/tools.py
# \namespace if1parser.tools
# \brief Parser Frontend
#
# This module contains a few tools that 
# are used when parsing if1
##

import sys
import log

##
# Print a warning to stdout.
#
# \param msg
#		The message to print
# \param line
#		The line where the warning was encountered
#		"?" is used if no line is provided.
#
# \todo Make this pass an error to the host application
#		when this runs embedded
##
def warning(msg, line = "?"):
	message = "line: " + line + ": " + msg
	log.logWarn("parser", message)

##
# Print an error to stdout.
# Quits the application after printing.
# You should only use this if correct execution is impossible.
# use warning() in other cases.
#
# \param msg
#		The message to print
# \param line
#		The line where the warning was encountered
#		"?" is used if no line is provided.
#
# \todo Make this pass an error to the host application
#		when this runs embedded
##
def error(msg, line = "?"):
	message = "line: " + line + ": " + msg
	log.logErr("parser", message)
	log.logErr("dvm", "Aborting after parse error.")
	sys.exit()