# instructions.py
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
# \package core.instruction
# \brief DVM instruction definitions
#
# This module defines the various instruction types.
##

import logging
log = logging.getLogger(__name__)

# -------------------- #
# Abstract Instruction #
# -------------------- #

##
# General DVM instruction.
#
# Defines an interface that all instructions should
# implement, along with some convenience functions.
##
class AbstractInstruction(object):
	def __init__(self):
		super(AbstractInstruction, self).__init__()
		self.key = None

	## Set the instruction address 
	def setKey(self, key):
		self.key = key

	## Return a string representation of this instruction.
	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"
	##
	# Execute an instruction with a given input
	# and a core.
	#
	# \param input
	#		A token, or a list of tokens, depending
	#		on the instruction type.
	# \param core
	#		The core where we execute this
	##
	def execute(self, input, core): pass

	## 
	# See if an instruction requires
	# context matching.
	##
	def needsMatcher(self): return False


# ------------------ #
# Static Instruction #
# ------------------ #

##
# A static instruction will always send it's 
# output to the same instructions.
#
# A static instruction can have multiple output ports.
# Furthermore, multiple destinations can exist for a single port.
##
class StaticInstruction(AbstractInstruction):
	def __init__(self):
		super(StaticInstruction, self).__init__()
		self.destinations = {}

	##
	# Add a destination to this instruction.
	#
	# \param port
	# 		The output port to link *from*
	# \param toInst
	#		The instruction to send to
	# \param toPort
	#		The port on this instruction to send to.
	##
	def addDestination(self, port, toInst, toPort):
		if port in self.destinations:
			self.destinations[port] += [(toInst, toPort)]
		else:
			self.destinations.update({port : [(toInst, toPort)]})

	##
	# Send a datum to any destination of a given output port.
	#
	# \param datum
	#		The piece of data to send.
	# \param core
	#		The currently active core.
	# \param port
	#		The port that we send outputs from.
	# \param cont
	#		The context of the output.
	##
	def sendDatum(self, datum, core, port, cont):
		for dst in self.destinations[port]:
			inst = dst[0]
			port = dst[1]
			core.tokenCreator.simpleToken(
				datum, inst, port, cont)

# ---------- #
# Operations #
# ---------- #

##
# An operation instruction defines a single operation
# on all of it's inputs.
##
class OperationInstruction(StaticInstruction):
	def needsMatcher(self): return True

	def __init__(self, operation, inputs):
		super(OperationInstruction, self).__init__()
		self.operation = operation
		self.inputs    = inputs

	##
	# Send results to the relevant destinations.
	#
	# Simply forwards any element in the list to all the
	# destinations of the matching output port of the instruction.
	# The length of results should be equal to the amount of output ports.
	##
	def sendResults(self, results, core, cont):
		for i in xrange(0, len(results)):
			res = results[i]
			self.sendDatum(res, core, i, cont)

	def execute(self, tokens, core):
		log.info("executing %s", self)
		lst = map(lambda x : x.datum, tokens)
		res = self.operation(*lst)
		cont = tokens[0].tag.cont
		self.sendResults([res], core, cont)		

# ----- #
# Sinks #
# ----- #

##
# Sink instruction.
#
# A sink is an instruction that only serves
# to forward any input it receives to it's destinations.
##
class Sink(StaticInstruction):
	def execute(self, token, core):
		port = token.tag.port
		cont = token.tag.cont
		datum = token.datum
		self.sendDatum(datum, core, port, cont)

# -------------- #
# Context Change #
# -------------- #

##
# Represents a context change in the program.
# e.g. a function call.
##
class ContextChange(AbstractInstruction):

	##
	# Initialize a context change instruction.
	#
	# \param destSink
	#		The destination of the tokens
	# \param returnSink
	#		The destination of the tokens 
	#		**after** their context is restored.
	##
	def __init__(self, destSink, returnSink):
		super(ContextChange, self).__init__()
		self.retnSink = returnSink
		self.destSink = destSink
		self.contexts = {}
		self.literals = {}

	def addLiteral(self, idx, lit):
		self.literals.update({idx : lit})

	def getLiterals(self):
		return self.literals

	def execute(self, token, core):
		log.info("%s, changing context of: %s", self, token)

		core.tokenCreator.changeContext(
			token,
			self,
			self.destSink,
			self.retnSink)

# --------------- #
# Context Restore #
# --------------- #

##
# Represents the restoration of context.
# e.g. returning from a function.
##
class ContextRestore(AbstractInstruction):
	def execute(self, token, core):
		log.info("%s, restoring: %s", self, token)
		core.tokenCreator.restoreContext(token)

# ----------------- #
# Meta Instructions #
# ----------------- #

##
# Represents the end of the program.
# Any input of this instruction is considered to be
# the result of the program.
##
class StopInstruction(AbstractInstruction):

	def execute(self, token, core):
		log.info("%s reached stop instruction: %s", token, self)
		core.tokenCreator.stopToken(token)