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

# ------------------ #
# Instruction Memory #
# ------------------ #

__CURRENT_STR_KEY__     = -1
__CURRENT_TLR_KEY__     = 0
__INSTRUCTION_MEMORY__ 	= {}

# Add a key in a given slot.
def _addInstruction(inst):
	__INSTRUCTION_MEMORY__.update({inst.key : inst})

def _reserveSTRSlot():
	global __CURRENT_STR_KEY__
	key = __CURRENT_STR_KEY__
	__CURRENT_STR_KEY__ -= 1
	return key

def _reserveTLRSlot():
	global __CURRENT_TLR_KEY__
	key = __CURRENT_TLR_KEY__
	__CURRENT_TLR_KEY__ += 1
	return key

# Get an instruction from the memory
def getInstruction(key):
	return __INSTRUCTION_MEMORY__[key]

# -------------------- #
# Instruction creation #
# -------------------- #

def _createInstruction(slotFunc, constructor, args = []):
	key 	= slotFunc()
	args	= [key] + args
	inst	= constructor(*args)
	_addInstruction(inst)
	return key

def addOperationInstruction(operation, inputs, outputs):
	return _createInstruction(_reserveTLRSlot, OperationInstruction, [inputs, outputs, operation])

def addForwardInstruction(slots):
	return _createInstruction(_reserveSTRSlot, ForwardInstruction, [slots])

def addCallInstruction(callRet):
	return _createInstruction(_reserveSTRSlot, CallInstruction, [callRet])

def addReturnInstruction():
	return _createInstruction(_reserveSTRSlot, ReturnInstruction, [])

def addStopInstruction():
	return _createInstruction(_reserveSTRSlot, StopInstruction, [])

# -------------------- #
# Abstract Instruction #
# -------------------- #

class AbstractInstruction(object):
	def __init__(self, key):
		super(AbstractInstruction, self).__init__()
		self.literals = []
		self.key      = key

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def acceptLiteral(self, literal):
		pass

# -------------- #
# Receiver Types #
# -------------- #

class ReceiverType(object):
	def run(self, input): pass
	def needsMatcher(self): pass

class SingleTokenReceiver(object):
	def acceptToken(self, token): pass
	def needsMatcher(self): return False
	def run(self, input):
		self.acceptToken(input)

class TokenListReceiver(object):
	def execute(self, tokens): pass
	def needsMatcher(self): return True
	def run(self, input):
		self.execute(input)

# ------------------ #
# Static Instruction #
# ------------------ #

class StaticInstruction(AbstractInstruction):
	def __init__(self, key, slots):
		super(StaticInstruction, self).__init__(key)
		self.destinations = [[] for x in xrange(0,slots)]
		self.slots = slots

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

# ------------------- #
# Dynamic Instruction #
# ------------------- #

class DynamicInstruction(AbstractInstruction, SingleTokenReceiver):
	def  modifyAndSend(self, token, inst, cont):
		token.tag.inst = inst
		token.tag.cont = cont
		runtime.addToken(token)

# ---------- #
# Operations #
# ---------- #

"""
Takes a list of tokens as input for it's internal function
"""

class OperationInstruction(StaticInstruction, TokenListReceiver):
	def __init__(self, key, inputs, outputs, operation):
		super(OperationInstruction, self).__init__(key, outputs)
		self.operation = operation
		self.inputs    = inputs

	def lift(self, literal): pass

	# Send a list of results
	# Every element in this list should have a matching output port
	def sendResults(self, results, cont):
		for i in xrange(0, len(results)):
			res = results[i]
			self.sendDatum(i, res, cont)

	def execute(self, tokens):
		print "['INS']", self, "executing", tokens
		lst = map(lambda x : x.datum, tokens)
		res = self.operation(*lst)
		cont = tokens[0].tag.cont
		self.sendResults([res], cont)		

# ------------------- #
# Forward Instruction #
# ------------------- #

"""
A forward instruction simply accepts a token and forwards it to 
it's destinations.
"""

class ForwardInstruction(StaticInstruction, SingleTokenReceiver):
	def __init__(self, key, slots):
		super(ForwardInstruction, self).__init__(key, slots)

	def acceptToken(self, token):
		print "['INS']", self, "forwarding", token
		port = token.tag.port
		cont = token.tag.cont
		datum = token.datum
		self.sendDatum(port, datum, cont)

# ---------------- #
# Call Instruction #
# ---------------- #

class CallInstruction(DynamicInstruction):
	def __init__(self, key, callRet):
		super(CallInstruction, self).__init__(key)
		self.func = None
		self.funcRet = None
		self.callRet = callRet
		self.contexts = {}

	def bind(self, func, funcRet):
		self.func = func
		self.funcRet = getInstruction(funcRet)

	def setReturn(self, newCont, oldCont):
		self.funcRet.attachReturn(newCont, oldCont, self.callRet)

	def getNewContext(self, oldCont):
		if oldCont not in self.contexts:
			newCont = context.createContext()
			self.contexts.update({oldCont : newCont})
			self.setReturn(newCont, oldCont)
			return newCont
		else:
			return self.contexts[oldCont]

	def acceptToken(self, token):
		print "['INS']", self, "calling", self.func, "with:", token
		oldCont = token.tag.cont
		newCont = self.getNewContext(oldCont)
		self.modifyAndSend(token, self.func, newCont)

# ------------------ #
# Return Instruction #
# ------------------ #

class ReturnInstruction(DynamicInstruction):
	def __init__(self, key):
		super(ReturnInstruction, self).__init__(key)
		self.map = {}

	def attachReturn(self, newCont, oldCont, target):
		self.map.update({newCont : (target, oldCont)})

	def acceptToken(self, token):
		print "['INS']", self, "returning", token
		pair = self.map[token.tag.cont]
		self.modifyAndSend(token, pair[0], pair[1])

# ---------------- #
# Stop Instruction #
# ---------------- #

class StopInstruction(DynamicInstruction):
	def __init__(self, key):
		super(StopInstruction, self).__init__(key)

	def acceptToken(self, token):
		print "['INS']", self, "stopping with token:", token
