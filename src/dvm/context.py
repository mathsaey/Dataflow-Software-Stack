# context.py
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


"""
Context creation

The following functions can be used by other modules:

createContext()
	Create and return a new context
literalContext()
	Return the context carried by every literal
"""

# -------------- #
# Context Object #
# -------------- #

class Context(object):
	def __init__(self, key):
		super(Context,self).__init__()
		self.key = key

	def __str__(self):
		return "Context: " + str(self.key)

	def __eq__(self, other):
		return other.key == self.key

	def __hash__(self):
		return self.key

# --------------- #
# Context creator #
# --------------- #

__CURRENT__ID__ = 0

def createContext():
	global __CURRENT__ID__
	__CURRENT__ID__ += 1
	return Context(__CURRENT__ID__ -1)

__LITCONTEXT__ = createContext()

def literalContext():
	return __LITCONTEXT__
