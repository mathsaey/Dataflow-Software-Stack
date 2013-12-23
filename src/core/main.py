# main.py
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

import Queue

# ---- #
# Port #
# ---- #

class Port(object):
	def __init__(self, instruction, idx):
		super(Port, self).__init__()
		self.instruction = instruction
		self.token = None
		self.idx = idx
     
	def __str__(self):
		return "Port " + str(self.idx) + " of instruction " + str(self.instruction)

	def acceptToken(self, token):
		print self, "accepted input:", token
		self.token = token

	def isReady(self):
		return self.token is not None

# ----------- #
# Instruction #
# ----------- #

class Instruction(object):
	def __init__(self, operation, inputs):
		super(Instruction, self).__init__()
		self.operation = operation
		self.destI = None
		self.destP = None
		self.inputs = [None] * inputs
		for idx in xrange(0, inputs):
			self.inputs[idx] = Port(self, idx)

	def __str__(self):
		return "Instruction: " + str(id(self))

	def setDestination(self, instruction, port):
		self.destI = instruction
		self.destP = port 

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
		return Token(self.destI, self.destP, datum)

	def execute(self):
		lst = self.gatherInput()
		res = self.operation(*lst)
		tok = self.createToken(res)
		addToken(tok)

# ----- #
# Token #
# ----- #

class Token(object):
	def __init__(self, instruction, port, datum):
		super(Token, self).__init__()
		self.instruction = instruction
		self.datum = datum
		self.port = port

	def __str__(self):
		dest = str(self.instruction) + " (" + str(self.port) + ")"
		summary = str(self.datum) + " | " + str(dest)
		return "Token (" + summary + ")"

	def send(self):
		print "Sending: ", self
		self.instruction.acceptToken(self)


# ------------------ #
# Instruction Memory #
# ------------------ #

__INSTRUCTION_MEMORY__ 	= {}

def addInstruction(key, instruction):
	__INSTRUCTION_MEMORY__.update({key:instruction})

def fetchInstruction(key):
	__INSTRUCTION_MEMORY__[key]

# ------- #
# Runtime #
# ------- #

__TOKEN__QUEUE__ = Queue.Queue()

def addToken(token):
	__TOKEN__QUEUE__.put(token)

def getToken():
	return __TOKEN__QUEUE__.get()

def run():
	 while True:
	 	t = getToken()
	 	t.send()

# ---- #
# Test #
# ---- #


def tOP(a,b):
	return a + b

def dummy(*any):
	pass

inst1 = Instruction(tOP, 2)
inst2 = Instruction(dummy, 1)
inst1.setDestination(inst2, 0)


t1 = Token(inst1, 0, "top")
t2 = Token(inst1, 1, "lel")

addToken(t1)
addToken(t2)

run()