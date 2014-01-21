# instructions.py
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
Create and retrieve instructions.

The following functions are available for use by other modules:

getInstruction(key)
	Get the instruction matching key

add<type>Instruction(args)
	Create and add an instruction of type
	the arguments depend on the type of the instruction
"""

import tokens
import runtime
import contextMatcher

# ------------------ #
# Instruction Memory #
# ------------------ #

__CURRENT_KEY__ = 0
__INSTRUCTION_MEMORY__ 	= []

# Add a key in a given slot.
def _addInstruction(inst):
	__INSTRUCTION_MEMORY__[inst.key] = inst

# Reserve a slot for an instruction
# returns the key of the reserved slot
def _reserveSlot():
	global __INSTRUCTION_MEMORY__
	global __CURRENT_KEY__
	__INSTRUCTION_MEMORY__ += [None]
	key = __CURRENT_KEY__
	__CURRENT_KEY__ += 1
	return key

# Get an instruction from the memory
def getInstruction(key):
	return __INSTRUCTION_MEMORY__[key]

# -------------------- #
# Instruction creation #
# -------------------- #

def _createInstruction(constructor, inputs, args):
	key 	= _reserveSlot()
	args	= [key] + args
	inst	= constructor(*args)
	contextMatcher.initLitArr(key, inputs)
	_addInstruction(inst)
	return key

def addOperationInstruction(operation, inputs):
	return _createInstruction(OperationInstruction, inputs, [operation])

# ----------- #
# Instruction #
# ----------- #

class AbstractInstruction(object):
	def __init__(self, key):
		super(AbstractInstruction, self).__init__()
		self.key     = key
		self.outputs = []

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def addDestination(self, port, toKey, toPort):
		self.outputs += [(toKey, toPort)]

	def sendDatum(self, datum):
		for o in self.outputs:
			key 	= o[0]
			port 	= o[1]
			token 	= tokens.createToken(key, port, 0, datum)
			runtime.addToken(token)

# --------------------- #
# Operation Instruction #
# --------------------- #

class OperationInstruction(AbstractInstruction):
	def __init__(self, key, operation):
		super(OperationInstruction, self).__init__(key)
		self.operation = operation

	def execute(self, lst):
		print self, "executing", lst
		res = self.operation(*lst)
		self.sendDatum(res)		
