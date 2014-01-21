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

def _createInstruction(constructor, inputs, outputs, args):
	key 	= _reserveSlot()
	args	= [key] + [inputs] + [outputs] + args
	inst	= constructor(*args)
	contextMatcher.initLitArr(key, inputs)
	_addInstruction(inst)
	return key

def addOperationInstruction(operation, inputs, outputs):
	return _createInstruction(OperationInstruction, inputs, outputs, [operation])

# ----------- #
# Instruction #
# ----------- #

class AbstractInstruction(object):
	def __init__(self, key, inputs, outputs):
		super(AbstractInstruction, self).__init__()
		self.key     = key
		self.inputs  = inputs
		self.outputs = outputs
		self.destinations = [[] for x in xrange(0,outputs)]

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def addDestination(self, port, toInst, toPort):
		self.destinations[port] += [(toInst, toPort)]

	# Send data on a given port to any destination
	# of this port
	def sendDatum(self, port, datum):
		for dst in self.destinations[port]:
			inst = dst[0]
			port = dst[1]
			token 	= tokens.createToken(inst, port, 0, datum)
			runtime.addToken(token)

	# Send a list of results
	# Every element in this list should have a matching output port
	def sendResults(self, results):
		for i in xrange(0, len(results)):
			res = results[i]
			self.sendDatum(i, res)

# --------------------- #
# Operation Instruction #
# --------------------- #

class OperationInstruction(AbstractInstruction):
	def __init__(self, key, inputs, outputs, operation):
		super(OperationInstruction, self).__init__(key, inputs, outputs)
		self.operation = operation

	def execute(self, tokens):
		print "['INSTRUCTION']", self, "executing", tokens
		lst = map(lambda x : x.datum, tokens)
		res = self.operation(*lst)
		self.sendResults([res])		

# -------------------- #
# Function Instruction #
# -------------------- #

class ForwardInstruction(AbstractInstruction):
	def __init__(self, key, inputs, outputs):
		super(ForwardInstruction, self).__init__(key, inputs, outputs)

	def acceptToken(self, token):
		self.sendDatum(token.tag.port, token.datum)
