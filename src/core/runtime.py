# runtime.py
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
This file defines the runtime system of the dynamic prototype.

The system has 2 responsibilities:
- Dispatching tokens that are available
- Determining which instruction to exectue
"""

import instructions
import Queue

# ---------------- #
# Public functions #
# ---------------- #

def run(): pass
def addToken(token): pass
def addInstruction(instruction, inputLst): pass

# ---------------- #
# Some Abstraction #
# ---------------- #

__TOKEN_QUEUE__ = Queue.Queue()
__INSTRUCTION_QUEUE__ = Queue.Queue()

def addToken(token): 
	__TOKEN_QUEUE__.put(token)
def addInstruction(instruction, inputLst):
	__INSTRUCTION_QUEUE__.put((instruction, inputLst))

def getToken(): return __TOKEN_QUEUE__.get()
def getInstruction(): return __INSTRUCTION_QUEUE__.get()




def sendToken(token):
	if token.key is None: return

	key = token.key
	dst = instructions.getInstruction(key)
	dst.acceptToken(token)

def run():
	 while True:
	 	t = getToken()
	 	sendToken(t)

