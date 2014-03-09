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

import subprocess
import tempfile
import IF1

##
# \package frontEnd.Sisal
# \author Mathijs Saey
# 
# \brief DISc Sisal FrontEnd.
#
# This module calls sisalc (has to be in your path), and uses the IF1
# frontend to parse the results.
#
# Since Sisalc seems to be unable to accept input from stdin, we use
# temporary files to interact with Sisal. 
##

def fromString(str):
	# Create a temp file and run sisalc on it
	file = tempfile.NamedTemporaryFile(suffix = '.sis', prefix = 'DIScTmp')
	name = file.name
	file.write(str)
	file.flush()

	subprocess.check_call(["sisalc", "-IF1", name])

	# Get the name of the output file
	name = name.replace('.sis', '.if1')

	# Open the file and run the IF1 frontend on it.
	file = open(name)
	IF1.fromString(file.read())
	file.close()