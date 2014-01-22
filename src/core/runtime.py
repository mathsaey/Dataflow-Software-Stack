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
Runtime system

The system has 2 responsibilities:
- Dispatching tokens that are available
- Determining which instruction to exectue

The following functions can be used by other modules:
run()
	Start the runtime
stop(token)
	Stop the runtime, the final token is returned to the user
addToken(token)
	Add a token to process
addInstruction(instruction, inputLst)
	Add an instruction that should be executed with
	the inputLst as argument
"""

import Queue
import threading
import instructions
import contextMatcher

# ------- #
# Storage #
# ------- #

__TOKEN_QUEUE__ = Queue.Queue()
__INSTRUCTION_QUEUE__ = Queue.Queue()

def addToken(token):
	print "['RUN']", "new token:", token 
	__TOKEN_QUEUE__.put(token)
def addInstruction(instruction, inputLst):
	print "['RUN']", "new instruction is ready:", instruction
	__INSTRUCTION_QUEUE__.put((instruction, inputLst))

def _getToken(): return __TOKEN_QUEUE__.get()
def _getInstruction(): return __INSTRUCTION_QUEUE__.get()

# -------- #
# Run Loop #
# -------- #

__ACTIVE__ = False

def _processToken(token):
	contextMatcher.addToken(token)

def _processInstruction(instruction, lst):
	inst = instructions.getInstruction(instruction)
	inst.execute(lst)

def _tokenLoop():
	while __ACTIVE__:
		token = _getToken()
		_processToken(token)

def _instructionLoop():
	while __ACTIVE__:
		inst = _getInstruction()
		_processInstruction(inst[0], inst[1])

def run():
	global __ACTIVE__
	__ACTIVE__ = True
	tokenThread = threading.Thread(target = _tokenLoop)
	instThread  = threading.Thread(target = _instructionLoop)
	tokenThread.start()
	instThread.start()
	tokenThread.join()
	instThread.join()

def stop(tokens):
	print "['RUN']", "Stop signal received", tokens
	global __ACTIVE__
	__ACTIVE__ = False