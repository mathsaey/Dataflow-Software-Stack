# runtime.py
# Mathijs Saey
# DVM

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
# \package DVM.runtime
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

import memory
import multiprocessing

from context import ContextCreator
from scheduler import Scheduler
from dispatcher import TokenDispatcher
from tokenCreator import TokenCreator
from contextMatcher import ContextMatcher

import logging
log = logging.getLogger(__name__)

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
	##
	# Initialize a core.
	#
	# This method only initializes all the components of the
	# core that are not dependent on multiprocessing elements.
	#
	# \param identifier
	#		The identifier of this core, this identifier should be unique 
	#		and it should match the identifier of this core in the collection
	#		of all the cores.
	# \param instructions
	#		A reference to the static instruction memory.
	##
	def __init__(self, identifier, memory):
		super(Core, self).__init__()
		log.info("Initializing core: %s")

		## Instruction memory
		self.memory         = memory
		## Identifier of this core. (integer)
		self.identifier     = identifier
		## See if this core is running.
		self.active         = True
		## Message Queue of this core
		self.inbox          = None
		## Message Queues of the other cores
		self.cores          = None

		## Context creator for this core
		self.contextCreator = ContextCreator(self)
		## Token creator for this core
		self.tokenCreator   = TokenCreator(self)
		## Token dispatcher for this core
		self.dispatcher     = TokenDispatcher(self)
		## Scheduler for this core
		self.scheduler      = Scheduler(self)
		## Context matcher for this core
		self.matcher        = ContextMatcher(self)

	## String representation of a core.
	def __str__(self):
		return "Core: " + str(self.identifier)

	## See if 2 cores are equal
	def __eq__(self, other):
		return self.identifier == other.identifier

	##
	# Add a token to the inbox of a core.
	#
	# \param token
	#		The token to add.
	# \param core
	#		The core to add the token to.
	#		The current core will be used if 
	#		this argument is not added.
	#
	def add(self, token, core = None):
		if core:
			self.cores[core].put(token)
		else: 
			self.inbox.put(token)

	## 
	# Set up the multiprocessing elements
	# of the core and start the runtime.
	#
	# \param inbox
	#		The message queue of this corec.
	# \param cores
	#		A list of the message queues of the
	#		other cores
	# \param logLock
	#		The lock of the logger.
	##
	def start(self, inbox, cores):
		self.inbox = inbox
		self.cores = cores

		log.info("Core %s starting run loop", self)

		while self.active:
			t = self.inbox.get()
			self.dispatcher.process(t)

	##
	# Stop the current core.
	#
	# \param value
	#		The result that the program
	#		returned.
	##
	def stop(self, value):
		log.info("Core %s terminated with %s", self, value)
		self.active = False
		print  value
		return value

##
# Initialize the cores, and start program execution.
#
# \param cores
#		The amount of cores to create.
##
def start(cores = 1, tokens = []):
	coreLst  = [Core(i, memory.memory()) for i in xrange(0, cores)]
	queues   = [multiprocessing.Queue()  for i in xrange(0, cores)]

	for i in xrange(0, cores):
		core  = coreLst[i]
		queue = queues[i]

		p = multiprocessing.Process(
			target = core.start, 
			name   = "C " + str(i),
			args   = (queue, queues)) 
		p.start()

	#-- DEBUG --#
	for t in tokens:
		queues[0].put(t)

