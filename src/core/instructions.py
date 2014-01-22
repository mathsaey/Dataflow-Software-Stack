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
import context
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

def _createInstruction(constructor, inputs, args = []):
	key 	= _reserveSlot()
	args	= [key] + [inputs] + args
	inst	= constructor(*args)
	contextMatcher.initLitArr(key, inputs)
	_addInstruction(inst)
	return key

def addOperationInstruction(operation, inputs, outputs):
	return _createInstruction(OperationInstruction, inputs, [outputs, operation])

def addForwardInstruction(inputs, outputs):
	return _createInstruction(ForwardInstruction, inputs, [outputs])

def addCallInstruction(inputs, callRet):
	return _createInstruction(CallInstruction, inputs, [callRet])

def addReturnInstruction(inputs):
	return _createInstruction(ReturnInstruction, inputs)

def addStopInstruction(inputs):
	return _createInstruction(StopInstruction, inputs)

# ------------ #
# Instructions #
# ------------ #

class AbstractInstruction(object):
	def __init__(self, key, inputs):
		super(AbstractInstruction, self).__init__()
		self.key     = key
		self.inputs  = inputs

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def execute(self, tokenList):
		raise NotImplementedError("Execute is an abstract method")

class StaticInstruction(AbstractInstruction):
	def __init__(self, key, inputs, outputs):
		super(StaticInstruction, self).__init__(key, inputs)
		self.destinations = [[] for x in xrange(0,outputs)]

	def addDestination(self, port, toInst, toPort):
		self.destinations[port] += [(toInst, toPort)]

	# Send data on a given port to any destination
	# of this port
	def sendDatum(self, port, datum, cont):
		for dst in self.destinations[port]:
			inst = dst[0]
			port = dst[1]
			token 	= tokens.createToken(inst, port, cont, datum)
			runtime.addToken(token)

	# Send a list of results
	# Every element in this list should have a matching output port
	def sendResults(self, results, cont):
		for i in xrange(0, len(results)):
			res = results[i]
			self.sendDatum(i, res, cont)

class DynamicInstruction(AbstractInstruction):
	def passModifiedToken(self, tokens, inst, cont):
		for token in tokens:
			token.tag.inst = inst
			token.tag.cont = cont
			runtime.addToken(token)

# ---------- #
# Operations #
# ---------- #

class OperationInstruction(StaticInstruction):
	def __init__(self, key, inputs, outputs, operation):
		super(OperationInstruction, self).__init__(key, inputs, outputs)
		self.operation = operation

	def execute(self, tokens):
		print "['INS']", self, "executing", tokens
		lst = map(lambda x : x.datum, tokens)
		res = self.operation(*lst)
		cont = tokens[0].tag.cont
		self.sendResults([res], cont)		

# --------- #
# Functions #
# --------- #

class ForwardInstruction(StaticInstruction):
	def __init__(self, key, inputs, outputs):
		super(ForwardInstruction, self).__init__(key, inputs, outputs)

	def execute(self, tokens):
		print "['INS']", self, "forwarding", tokens
		lst = map(lambda x : x.datum, tokens)
		cont = tokens[0].tag.cont
		self.sendResults(lst, cont)	

class CallInstruction(DynamicInstruction):
	def __init__(self, key, inputs, callRet):
		super(CallInstruction, self).__init__(key, inputs)
		self.func = None
		self.funcRet = None
		self.callRet = callRet

	def bind(self, func, funcRet):
		self.func = func
		self.funcRet = getInstruction(funcRet)

	def setReturn(self, newCont, oldCont):
		self.funcRet.attachReturn(newCont, oldCont, self.callRet)

	def execute(self, tokens):
		print "['INS']", self, "calling", self.func, "with:", tokens
		newCont = context.createContext()
		oldCont = tokens[0].tag.cont
		self.setReturn(newCont, oldCont)
		self.passModifiedToken(tokens, self.func, newCont)	

class ReturnInstruction(DynamicInstruction):
	def __init__(self, key, inputs):
		super(ReturnInstruction, self).__init__(key, inputs)
		self.map = {}

	def attachReturn(self, newCont, oldCont, target):
		self.map.update({newCont : (target, oldCont)})

	def execute(self, tokens):
		print "['INS']", self, "returning", tokens
		pair = self.map[tokens[0].tag.cont]
		self.passModifiedToken(tokens, pair[0], pair[1])

# ----- #
# Other #
# ----- #

class StopInstruction(DynamicInstruction):
	def __init__(self, key, inputs):
		super(StopInstruction, self).__init__(key, inputs)

	def execute(self, tokens):
		print "['INS']", self, "stopping"
		runtime.stop(tokens)
