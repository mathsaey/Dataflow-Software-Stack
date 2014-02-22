# literal.py
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
# \package IGR.literal
# \brief Literal definitions
# 
# IGR Literals
##

##
# Literal
#
# Literals are values inherent to the program.
# Examples include constants in arithmetic expressions,
# function names, strings, ...
# 
# Every literal has a value and a target, which is an igr::port::InputPort.
##
class Literal(object):
	
	##
	# Create a new literal.
	#
	# \param value
	#		The value of the literal
	# \param destination
	#		The destination of the literal value
	##
	def __init__(self, value, destination):
		super(Literal, self).__init__()
		self.value = value
		self.destination = destination

	## See if this is a port (mainly for traversal)
	def isPort(self): return False