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

##
# \file dvm/rumtime.py
# \namespace dvm.runtime
# \brief DVM runtime core
# 
# This module defines the runtime. 
# The runtime is responsible for dispatching tokens,
# matching tokens by their contexts and for scheduling
# instructions that are ready to execute.
#
# Multiple runtime "cores" are active at any given time, depending
# on the system. It is the responsibility of the runtime to find a
# decent load balance accross these cores.
##

import instructions
import multiprocessing

# ------------- #
# Runtime Class #
# ------------- #

##
# Runtime core.
#
# A runtime core is a worker unit in DVM.
# It defines it's own scheduler, matcher and
# token dispatcher and it has a static copy of the
# instruction memory.
##
class Core(object):
	def __init__(self):
		super(Core, self).__init__()
		self.active         = False
		self.instructions   = None
		self.contextCreator = None

		self.dispatcher = TokenDispatcher(self)
		self.scheduler  = Scheduler(self)
		self.matcher    = ContextMatcher(self)



class RuntimeObject(object):

	def __init__(self, core):
		super(RuntimeObject, self).__init__()
		self.core = core

# ---------------- #
# Token Dispatcher #
# ---------------- #

class TokenDispatcher(RuntimeObject):

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

