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

# ------ #
# Tokens #
# ------ #

class Token(object):
	def __init__(self, destination, port, datum):
		super(Token, self).__init__()
		self.destination = destination
		self.datum = datum
		self.port = port
	def getDestination(self): self.destination
	def getDatum(self): self.datum
	def getPort(self): self.port

# ------------- #
# Insctructions #
# ------------- #

class Instruction(object):

	def __init__(self, operation, inputs, outputs):
		super(Instruction, self).__init__()

	def execute(self):
		self.operation(*input)

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
	__TOKEN__QUEUE__.get()
