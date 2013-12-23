# instructions.py
# Mathijs Saey
# dvm prototype

# The MIT License (MIT)
#
# Copyright (c) 2013 Mathijs Saey
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
This file allows the user to create and retrieve instructions
"""

import copy
import port
import token
import runtime

# ---------------- #
# Public functions #
# ---------------- #

""" Creates an instruction and returns it's key """
def createInstruction(operation, inputs): pass
""" Retrieve an instruction with a given key """
def getInstruction(key): pass

# ------------- #
# Key Generator #
# ------------- #

__KEY__ = 1

def getKey():
	global __KEY__
	__KEY__ += 1
	return __KEY__ - 1

# ------------------ #
# Instruction Memory #
# ------------------ #

__INSTRUCTION_MEMORY__ 	= {}

def createInstruction(operation, inputs):
	inst = Instruction(operation, getKey(), inputs)
	__INSTRUCTION_MEMORY__.update({inst.key:inst})
	return inst.key

def getInstruction(key):
	return __INSTRUCTION_MEMORY__[key]

# ----------- #
# Instruction #
# ----------- #

class Instruction(object):
	def __init__(self, operation, key, inputs):
		super(Instruction, self).__init__()
		self.operation 	= operation
		self.nextPort	= None
		self.nextKey 	= None
		self.key 		= key

		self.inputs = [None] * inputs
		for idx in xrange(0, inputs):
			self.inputs[idx] = port.Port(self, idx)

	def __str__(self):
		return "Instruction: " + "'" + str(self.key) + "'"

	def setNext(self, key, port):
		self.nextPort 	= port
		self.nextKey	= key

	def isReady(self):
		for el in self.inputs:
			if (el is None) or not el.isReady():
				return False
    		return True

	def acceptToken(self, token):
		port = self.inputs[token.port]
		port.acceptToken(token)
		if self.isReady(): self.execute()

	def gatherInput(self):
		resLst = []
		for el in self.inputs: 
			resLst += [el.token.datum]
		return resLst

	def createToken(self, datum):
		return token.Token(self.nextKey, self.nextPort, datum)

	def execute(self):
		lst = self.gatherInput()
		res = self.operation(*lst)
		tok = self.createToken(res)
		runtime.addToken(tok)