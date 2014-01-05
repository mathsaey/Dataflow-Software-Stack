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

import tokens
import runtime
import context

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
	def __init__(self, key, inputs, outputs):
		super().__init__()
		self.key 			= key
		self.tokens			= {}
		self.inputs 		= inputs
		self.outputs 		= outputs
		self.destinations 	= [None] * self.outputs

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def setNext(self, output, key, port):
		self.destinations[output] = (key, port)

	def sendToken(self):
		pass

	def createToken(self, datum):
		return tokens.Token(
			self.nextKey, 
			self.nextPort, 
			datum, 
			#context.createContext())
			0)

	def acceptToken(self, token):
		print(self, "accepting", token)
		cont = token.context
		
		try:
			arr = self.tokens[cont]
			arr[token.port] = token
		except KeyError:
			arr = [None] * self.inputs
			arr[token.port] = token
			self.tokens.update({cont : arr})

	def isContextComplete(self, context):
		try:
			arr = self.tokens[context]
		except KeyError:
			return False
		else:
			return arr.count(None) == 0

	def grabData(self, context):
		lst = self.tokens[context]
		return map(lambda x : x.datum, lst)

# --------------------- #
# Operation Instruction #
# --------------------- #

class OperationInstruction(Instruction):
	def __init__(self, key, operation, inputs, outputs):
		super().__init__(key, inputs, outputs)
		self.operation = operation

	def __str__(self):
		str = super().__str__()
		return "Operation " + str

	def acceptToken(self, token):
		super().acceptToken(self, token)
		cont = token.context
		if self.isContextComplete(cont):
			pass

	def execute(self, context):
		args 	= self.grabData(context)
		res 	= self.operation(*args)
		tok 	= self.createToken(res)
		runtime.addToken(tok)

# -------------------- #
# Function Instruction #
# -------------------- #

class FunctionInstruction(Instruction):
	def __init__(self, inputs, outputs):
		super().__init__()
	
# ---------------- #
# Call Instruction #
# ---------------- #

class CallInstruction(Instruction):
	def __init__(self, inputs, outputs):
		super().__init__()
		self.inputKey = None
		self.outputKey = None

	def setTarget(self, key):
		self.key = key	