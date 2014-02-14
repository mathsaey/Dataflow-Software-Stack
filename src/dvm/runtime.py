# runtime.py
# Mathijs Saey
# dvm

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
		self.instructionMemory = None
		self.schedulerQueue    = None
		self.contextQueue      = None
		self.tokenQueue        = None
		self.logLock           = None
		self.working           = False

	def addData(self, 
			instructionMemory = None,
			schedulerQueue = None, 
			contextQueue = None, 
			tokenQueue = None,
			logLock = None,
			):

		self.instructionMemory = instructionMemory
		self.schedulerQueue = schedulerQueue
		self.contextQueue = contextQueue
		self.tokenQueue = tokenQueue
		self.logLock = logLock

	def stop(self):
		self.schedulerQueue.put(__STOP__)
		self.contextQueue.put(__STOP__)
		self.tokenQueue.put(__STOP__)

	def addInstruction(self, inst, input):
		self.schedulerQueue.put((inst, input))
	def addToken(self, token):
		self.tokenQueue.put(token)
	def addToContext(self, token):
		self.contextQueue.put(token)

	def process(self, obj): pass

	def log(self, name, *strings):
		tail = ""
		name = "['" + name + "']"
		for s in strings:
			tail += str(s) + " "
		with self.logLock:
			print name + tail

	def runLoop(self):
		self.working = True
		while self.working:
			message = self.messages.get()
			if message == __STOP__:
				self.working = False
			else:
				self.process(message)

# --------------- #
# Context Matcher #
# --------------- #

class ContextMatcher(RuntimeObject):

	def __init__(self):
		super(ContextMatcher, self).__init__()
		self.tokens = {}

	# See if we have a token array for a key, 
	# create one if we don't
	def checkKey(self, key):
		if key not in self.tokens:
			inst = self.instructionMemory.get(key[0])
			inputs = inst.inputs
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

# ---------------- #
# Token Dispatcher #
# ---------------- #

class TokenDispatcher(RuntimeObject):

	def __init__(self):
		super(TokenDispatcher, self).__init__()

	def processToken(self, token):
		inst = token.tag.inst
		if inst < 0:
			self.addInstruction(inst, token)
		else:
			self.addToContext(token)

	def process(self, obj):
		self.processToken(obj)

# --------- #
# Scheduler #
# --------- #

class Scheduler(RuntimeObject):
	def processInstruction(self, pair):
		inst = self.instructionMemory.get(pair[0])
		inst.run = self
		inst.execute(pair[1])

	def process(self, obj):
		self.processInstruction(obj)

# -------- #
# Run Loop #
# -------- #

def runProc(runtimeObj):
	runtimeObj.runLoop()

__TOKENS__ = []

def addToken(token):
	__TOKENS__.append(token)

def run():

	t = TokenDispatcher()
	c = ContextMatcher()
	s = Scheduler()

	lock = multiprocessing.Lock()
	tQ = t.messages
	cQ = c.messages
	sQ = s.messages

	t.addData(instructionMemory = instructions.__INSTRUCTIONS__,
				 schedulerQueue = sQ, contextQueue = cQ, tokenQueue = tQ, logLock = lock)
	c.addData(instructionMemory = instructions.__INSTRUCTIONS__,
				 schedulerQueue = sQ, contextQueue = cQ, tokenQueue = tQ, logLock = lock)
	s.addData(instructionMemory = instructions.__INSTRUCTIONS__,
				 schedulerQueue = sQ, contextQueue = cQ, tokenQueue = tQ, logLock = lock)

	for token in __TOKENS__:
		t.addToken(token)

	tProc = multiprocessing.Process(target = runProc, args = (t,), name = "TokenDispatcher")
	cProc = multiprocessing.Process(target = runProc, args = (c,), name = "Context Matcher")
	sProc = multiprocessing.Process(target = runProc, args = (s,), name = "Scheduler")

	print "[RUN]", "starting processes..."

	tProc.start()
	cProc.start()
	sProc.start()

	tProc.join()
	cProc.join()
	sProc.join()

	print "[RUN]", "runtime has finished..."

