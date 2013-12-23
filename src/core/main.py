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

# ----- #
# Token #
# ----- #

class Token(object):
	def __init__(self, iKey, iPort, datum):
		super(Token, self).__init__()
		self.datum = datum
		self.iPort = iPort
		self.iKey = iKey

	def __str__(self):
		dest = str(self.iKey) + " (" + str(self.iPort) + ")"
		summary = str(self.datum) + " | " + str(dest)
		return "Token (" + summary + ")"

	def send(self, destination):
		print "Sending:", self, "to", destination
		destination.acceptToken(self)

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
	def __init__(self, operation, key, inputs):
		super(Instruction, self).__init__()
		self.operation = operation
		self.nextI 	= None
		self.nextP 	= None
		self.key 	= key

		self.inputs = [None] * inputs
		for idx in xrange(0, inputs):
			self.inputs[idx] = Port(self, idx)

	def __str__(self):
		return "Instruction: " + "'" + str(self.key) + "'"

	def setNext(self, instruction, port):
		self.nextI = instruction
		self.nextP = port 

	def isReady(self):
		for el in self.inputs:
			if (el is None) or not el.isReady():
				return False
    		return True

	def acceptToken(self, token):
		port = self.inputs[token.iPort]
		port.acceptToken(token)
		if self.isReady(): self.execute()

	def gatherInput(self):
		resLst = []
		for el in self.inputs:
			resLst += [el.token.datum]
		return resLst

	def createToken(self, datum):
		return Token(self.nextI, self.nextP, datum)

	def execute(self):
		lst = self.gatherInput()
		res = self.operation(*lst)
		tok = self.createToken(res)
		addToken(tok)

# ------------------ #
# Instruction Memory #
# ------------------ #

__INSTRUCTION_MEMORY__ 	= {}

def addInstruction(instruction):
	__INSTRUCTION_MEMORY__.update({instruction.key:instruction})

def fetchInstruction(key):
	return __INSTRUCTION_MEMORY__[key]

# ------- #
# Runtime #
# ------- #

__TOKEN__QUEUE__ = Queue.Queue()

def addToken(token):
	__TOKEN__QUEUE__.put(token)

def getToken():
	return __TOKEN__QUEUE__.get()

def sendToken(token):
	if token.iKey is None: return

	key = token.iKey
	dst = fetchInstruction(key)
	token.send(dst)

def run():
	 while True:
	 	t = getToken()
	 	sendToken(t)

# ---- #
# Test #
# ---- #


def tOP(a,b):
	return a + b

def dummy(*any):
	pass

inst1 = Instruction(tOP, "test instruction 1", 2)
inst2 = Instruction(dummy, "end test instruction",1)
inst1.setNext("end test instruction", 0)

addInstruction(inst1)
addInstruction(inst2)

t1 = Token("test instruction 1", 0, "top")
t2 = Token("test instruction 1", 1, "lel")

addToken(t1)
addToken(t2)

run()