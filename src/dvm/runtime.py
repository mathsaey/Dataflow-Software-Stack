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

import log
import memory
import multiprocessing

from context import ContextCreator
from scheduler import Scheduler
from dispatcher import TokenDispatcher
from tokenCreator import TokenCreator
from contextMatcher import ContextMatcher

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
	# \param logLock
	#		The lock of the log module of the parent process.
	# \param prefix
	#		The prefix of this core, this prefix should be unique 
	#		and it should match the index of this core in the collection
	#		of all the cores.
	# \param instructions
	#		A reference to the static instruction memory.
	##
	def __init__(self, logLock = None, prefix = None, memory = None):
		super(Core, self).__init__()
		log.setLock(logLock)
		log.info("core", "Initializing core: " + str(prefix))

		## Instruction memory
		self.memory         = memory
		## Identifier of this core. (integer)
		self.prefix         = prefix
		## See if this core is running.
		self.active         = True
		## References to the other active cores.
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

	##
	# Update the core with references
	# to the other cores.
	##
	def link(self, cores):
		self.cores = cores

	## 
	# Main run loop of the core.
	# Keeps on serving tokens, which are in turn
	# processed by the token dispatcher until a stop
	# token is encountered, at which point the dispatcher
	# will stop this core.
	##
	def run(self):
		log.info("core", "(" + str(self.prefix) + ") Starting run loop")
		while self.active:
			self.dispatcher.cycle()
		log.info("core", "(" + str(self.prefix) + ") Terminated")

##
# Initialize the cores, and start program execution.
#
# \param cores
#		The amount of cores to create.
##
def start(cores = 1, tokens = []):

	logLock = log.getLock()
	coreList = [None] * cores

	for i in xrange(0, cores):
		coreList[i] = Core(
			memory  = memory.memory(),
			logLock = logLock,
			prefix  = i
			)

	## DEBUG
	for t in tokens:
		coreList[0].dispatcher.add(t)

	for core in coreList:
		core.link(coreList)
		p = multiprocessing.Process(target = core.run(), name = core.prefix)
		p.start()
