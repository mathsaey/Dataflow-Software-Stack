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

# ------------------ #
# Instruction Memory #
# ------------------ #

class InstructionMemory(object):

	def __init__(self):
		super(InstructionMemory, self).__init__()
		self.memory = {}
		self.strKey = -1
		self.trlKey = 0

	def getInstruction(self, key):
		return self.memory[key]

	def reserveSTRSlot(self):
		key = self.strKey
		self.strKey -= 1
		return key

	def reserveTLRSlot(self):
		key = self.trlKey
		self.trlKey += 1
		return key

	def addInstruction(self, inst):
		key = None

		if inst.isSTR():
			key = self.reserveSTRSlot()
		elif inst.isTLR():
			key = self.reserveTLRSlot()
		else:
			print "INS", "Memory received invalid instruction", inst

		self.memory.update({key : inst})
		inst.setMemory(key, self)
		return key

	def get(self, key):
		return self.memory[key]

	def reset(self):
		self.__init__()

# -------------------- #
# Instruction creation #
# -------------------- #

__INSTRUCTIONS__ = InstructionMemory()

def getInstruction(key):
	return __INSTRUCTIONS__.get(key)

def createInstruction(constructor, args = []):
	inst = constructor(*args)
	key = __INSTRUCTIONS__.addInstruction(inst)
	return key

def addOperationInstruction(operation, inputs):
	return createInstruction(OperationInstruction, [inputs, operation])
def addContextChange(callRet):
	return createInstruction(ContextChange, [callRet])
def addSink(): 
	return createInstruction(Sink, [])
def addContextRestore():
	return createInstruction(ContextRestore, [])
def addStopInstruction():
	return createInstruction(StopInstruction, [])

# -------------------- #
# Abstract Instruction #
# -------------------- #

class AbstractInstruction(object):
	def __init__(self):
		super(AbstractInstruction, self).__init__()
		self.key      = None
		self.mem 	  = None
		self.run 	  = None

	def setMemory(self, key, mem):
		self.key = key
		self.mem = mem

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

# -------------- #
# Receiver Types #
# -------------- #

class ReceiverType(object):
	def isSTR(self): pass
	def isTLR(self): pass

	def execute(self, input): pass
	def needsMatcher(self): pass

class SingleTokenReceiver(ReceiverType):
	def needsMatcher(self): return False
	def isSTR(self): return True
	def isTLR(self): return False

	def acceptToken(self, token): pass
	def execute(self, input):
		self.acceptToken(input)

class TokenListReceiver(ReceiverType):
	def needsMatcher(self): return True
	def isSTR(self): return False
	def isTLR(self): return True

	def acceptList(self, tokens): pass
	def execute(self, input):
		self.acceptList(input)

# ------------------ #
# Static Instruction #
# ------------------ #

class StaticInstruction(AbstractInstruction):
	def __init__(self):
		super(StaticInstruction, self).__init__()
		self.destinations = {}

	def addDestination(self, port, toInst, toPort):
		if port in self.destinations:
			self.destinations[port] += [(toInst, toPort)]
		else:
			self.destinations.update({port : [(toInst, toPort)]})

	# Send data on a given port to any destination
	# of this port
	def sendDatum(self, port, datum, cont):
		for dst in self.destinations[port]:
			inst = dst[0]
			port = dst[1]
			token 	= tokens.createToken(inst, port, cont, datum)
			self.run.addToken(token)

# ------------------- #
# Dynamic Instruction #
# ------------------- #

class DynamicInstruction(AbstractInstruction, SingleTokenReceiver):
	def  modifyAndSend(self, token, inst, cont):
		token.tag.inst = inst
		token.tag.cont = cont
		self.run.addToken(token)

# ---------- #
# Operations #
# ---------- #

"""
Takes a list of tokens as input for it's internal function
"""

class OperationInstruction(StaticInstruction, TokenListReceiver):
	def __init__(self, inputs, operation):
		super(OperationInstruction, self).__init__()
		self.operation = operation
		self.inputs    = inputs

	# Send a list of results
	# Every element in this list should have a matching output port
	def sendResults(self, results, cont):
		for i in xrange(0, len(results)):
			res = results[i]
			self.sendDatum(i, res, cont)

	def acceptList(self, tokens):
		self.run.log("INS", self, "executing", tokens)
		lst = map(lambda x : x.datum, tokens)
		res = self.operation(*lst)
		cont = tokens[0].tag.cont
		self.sendResults([res], cont)		

# ----- #
# Sinks #
# ----- #

class Sink(StaticInstruction, SingleTokenReceiver):

	def acceptToken(self, token):
		self.run.log("INS", self, "forwarding", token)
		port = token.tag.port
		cont = token.tag.cont
		datum = token.datum
		self.sendDatum(port, datum, cont)

# -------------- #
# Context Change #
# -------------- #

class ContextChange(DynamicInstruction):
	def __init__(self, returnSink):
		super(ContextChange, self).__init__()
		self.returnSink = returnSink
		self.entrySink  = None
		self.restore    = None
		self.contexts = {}

	def bind(self, entrySink, restore):
		self.entrySink = entrySink
		self.restore = self.mem.get(restore)

	def setRestore(self, newCont, oldCont):
		self.restore.attachSink(newCont, oldCont, self.returnSink)

	def getContext(self, oldCont):
		if oldCont not in self.contexts:
			newCont = context.createContext()
			self.contexts.update({oldCont : newCont})
			self.setRestore(newCont, oldCont)
			return newCont
		else:
			return self.contexts[oldCont]

	def acceptToken(self, token):
		self.run.log("INS", self, "calling", self.entrySink, "with:", token)
		oldCont = token.tag.cont
		newCont = self.getContext(oldCont)
		self.modifyAndSend(token, self.entrySink, newCont)

# --------------- #
# Context Restore #
# --------------- #

class ContextRestore(DynamicInstruction):
	def __init__(self):
		super(ContextRestore, self).__init__()
		self.map = {}

	def attachSink(self, newCont, oldCont, target):
		self.map.update({newCont : (target, oldCont)})

	def acceptToken(self, token):
		self.run.log("INS", self, "restoring", token)
		pair = self.map[token.tag.cont]
		self.modifyAndSend(token, pair[0], pair[1])

# ----------------- #
# Meta Instructions #
# ----------------- #

class StopInstruction(DynamicInstruction):

	def acceptToken(self, token):
		self.run.log("INS", self, "stopping with token:", token)
		self.run.stop()
