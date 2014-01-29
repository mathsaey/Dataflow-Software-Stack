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

import log
import instructions
import multiprocessing

# ------------- #
# Runtime Class #
# ------------- #

__STOP__ = "<|Stop|>"

class RuntimeObject(object):
	def __init__(self):
		super(RuntimeObject, self).__init__()
		self.messages = multiprocessing.Queue()
		self.schedulerQueue = []
		self.contextQueue   = []
		self.tokenQueue     = []
		self.logLock        = []
		self.working        = False

	def setQueues(self, 
			schedulerQueue = None, 
			contextQueue = None, 
			tokenQueue = None):

		self.schedulerQueue = schedulerQueue
		self.contextQueue = contextQueue
		self.tokenQueue = tokenQueue

	def addInstruction(self, inst, input):
		self.schedulerQueue.put((inst, input))
	def addToken(self, token):
		self.tokenQueue.put(token)
	def addToContext(self, token):
		self.contextQueue.put(token)

	def process(self, obj): pass

	def log(self, message):
		with logLock:
			print "[RUN]", message

	def runLoop(self):
		self.working = True
		while self.working:
			message = self.messages.get()
			if message == __STOP__:
				self.working = False
			else:
				self.process(message)

# --------------- #
# Runtime Classes #
# --------------- #

class ContextMatcher(RuntimeObject):

	def __init__(self):
		super(ContextMatcher, self).__init__()
		self.operations = {}
		self.tokens = {}

	# Add the amount of inputs a given instruction
	# will accept. Should be done while adding instructions.
	def addInstruction(self, key, inputs):
		self.operations.update({key : inputs})

	# See if we have a token array for a key, 
	# create one if we don't
	def checkKey(self, key):
		if key not in self.tokens:
			inputs = self.operations[key[0]]
			arr = [None] * inputs
			self.tokens.update({key : arr})

	# Update the token array for a key
	def updateKeyArr(self, key, port, token):
		arr = self.tokens[key]
		arr[port] = token
	
	# See if a given key is ready to execute
	def isKeyReady(self, key):
		return self.tokens[key].count(None) == 0

	# Execute an instruction that's ready
	def executeKey(self, key):
		arr = self.tokens[key]
		del self.tokens[key]
		self.addInstruction(key[0], arr)

	# Add a token to the matcher
	def processToken(self, token):
		tag  = token.tag                  
		inst = tag.inst                   
		cont = tag.cont                   
		port = tag.port                   
		key  = (inst, cont)

		self.checkKey(key)
		self.updateKeyArr(key, port, token)

		if self.isKeyReady(key):
			self.executeKey(key)

	def process(self, obj): 
		self.processToken(obj)


class TokenDispatcher(RuntimeObject):

	def __init__(self, contextQueue):
		super(TokenDispatcher, self).__init__()

	def processToken(self, token):
		inst = token.tag.inst
		if inst < 0:
			self.addInstruction(inst, token)
		else:
			self.addToContext(token)

	def process(self, obj):
		self.processToken(obj)

class Scheduler(RuntimeObject):
	def processInstruction(self, obj):




def _processInstruction(instruction, input):
	inst = instructions.getInstruction(instruction)
	inst.run(input)

def _tokenLoop():
	while __ACTIVE__:
		token = _getToken()
		_processToken(token)

def _instructionLoop():
	while __ACTIVE__:
		inst = _getInstruction()
		_processInstruction(inst[0], inst[1])

def run():
	log.log("RUN", "starting runtime")
	global __ACTIVE__
	__ACTIVE__ = True
	tokenThread = threading.Thread(target = _tokenLoop)
	instThread  = threading.Thread(target = _instructionLoop)
	tokenThread.start()
	instThread.start()
	tokenThread.join()
	instThread.join()
	log.log("RUN", "runtime has finished")
