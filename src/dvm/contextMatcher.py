# contextMatcher.py
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
Context matcher.

The context matcher is responsible for gathering tokens
with the same context before sending them to the instruction they belong to.
"""

import runtime

# ------- #
# Matcher #
# ------- #

class ContextMatcher(object):

	def __init__(self):
		super(ContextMatcher, self).__init__()
		self.operations = {}
		self.tokens = {}

	# Add the amount of inputs a given instruction
	# will accept. Should be done while adding instructions.
	def addInstruction(self, key, inputs):
		self.operations.update({key : inputs})

	# See if we have a token array for a key, 
	# create one if we don't
	def checkKey(self, key):
		if key not in self.tokens:
			inputs = self.operations[key[0]]
			arr = [None] * inputs
			self.tokens.update({key : arr})

	# Update the token array for a key
	def updateKeyArr(self, key, port, token):
		arr = self.tokens[key]
		arr[port] = token
	
	# See if a given key is ready to execute
	def isKeyReady(self, key):
		return self.tokens[key].count(None) == 0

	# Execute an instruction that's ready
	def executeKey(self, key):
		arr = self.tokens[key]
		del self.tokens[key]
		runtime.addInstruction(key[0], arr)

	# Add a token to the matcher
	def processToken(self, token):
		tag  = token.tag                  
		inst = tag.inst                   
		cont = tag.cont                   
		port = tag.port                   
		key  = (inst, cont)

		self.checkKey(key)
		self.updateKeyArr(key, port, token)

		if self.isKeyReady(key):
			self.executeKey(key)

	def process(self, x): 
		self.processToken(x)