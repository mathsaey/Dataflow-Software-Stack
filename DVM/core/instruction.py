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

	##
	# Add a literal to the operation.
	# An instruction should never accept only
	# literals.
	# Not all instructions accept literals.
	##
	def addLiteral(self, port, val):
		log.error("Invalid literal: %s added to instruction: %s", val, self)


## DVM instruction that has a list of outputs.
class DestinationListInstruction(AbstractInstruction):

	def __init__(self):
		self.destinations = []

	##
	# Add a destination to this instruction.
	#
	# \param inst
	#		The instruction to send the output to.
	# \param _ 
	#		This is an argument that is used to define the 
	#		output port, when this method is called on a sink.
	#		It is ignored for operationInstructions.
	# \param port
	#		The port to send the output to.
	##
	def addDestination(self, _, inst, port):
		self.destinations.append((inst, port))

	##
	# Send a datum to all of the destinations.
	#
	# \param datum
	#		The datum to send
	# \param core
	#		The core to utilise
	# \param cont
	#		The context of the token that will be created.
	##
	def sendDatum(self, datum, core, cont):
		for dst in self.destinations:
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
class OperationInstruction(DestinationListInstruction):
	def needsMatcher(self): return True

	def __init__(self, operation, inputs):
		super(OperationInstruction, self).__init__()
		self.totalinputs  = inputs
		self.realInputs   = inputs
		self.operation    = operation
		self.litLst       = [None] * inputs

	def addLiteral(self, port, val):
		self.litLst[port] = val
		self.realInputs -= 1

	##
	# Replace all empty places in the 
	# argument list by literals, extract
	# the datum from tokens and get the context
	# from one of the tokens.
	##
	def createArgLst(self, args):
		cont = None

		for i in xrange(0, len(args)):
			el = args[i]
			if el:
				cont = el.tag.cont
				args[i] = el.datum
			else: 
				args[i] = self.litLst[i]

		return (cont, args)

	def execute(self, tokens, core):
		log.info("executing %s", self)
		cont, lst = self.createArgLst(tokens)
		res = self.operation(*lst)
		self.sendDatum(res, core, cont)		

# -------- # 
# Constant #
# -------- #

##
# Constant instruction.
#
# A special sink that always sends it's value
# to it's destinations when it encounters input.
# This is not really 'nice' according to dataflow 
# semantics but necessary to allow literals that cannot
# be propagated.
##
class Constant(DestinationListInstruction):

	def __init__(self, value):
		super(Constant, self).__init__()
		self.value = value

	def execute(self, token, core):
		self.sendDatum(self.value, core, token.tag.cont)

# ----- #
# Sinks #
# ----- #

##
# Sink instruction.
#
# A sink is an instruction that only serves
# to forward any input it receives to it's destinations.
##
class Sink(AbstractInstruction):
	def __init__(self):
		super(Sink, self).__init__()
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
		self.literals = {}

	def addLiteral(self, port, val):
		self.literals.update({port : val})

	def getLiterals(self):
		return self.literals

	def execute(self, token, core):
		log.info("%s, changing context of: %s", self, token)

		core.tokenCreator.changeContext(token, self)

##
# Represents an instruction that will dynamically
# determine the destination of it's tokens at runtime.
#
# The value of the token arriving at port 0 will determine
# the next goal of the tokens. Tokens that arrive before this
# token will be stored until their destination is resolved.
#
# This value should be an index corresponding to an entry in
# the dstLst of the instruction. This entry is the destination of
# the tokens that this instruction receives (for this context).
##
class Switch(AbstractInstruction):

	def __init__(self, dstLst):
		super(Switch, self).__init__()
		self.dstLst = dstLst

	def getDst(self, token):
		try:
			return self.dstLst[token.datum]
		except IndexError:
			log.error("%s: Invalid switch destination idx: %s, using 0", self, token.datum)
			return self.dstLst[0]

	def execute(self, token, core):
		port = token.tag.port

		if port == 0:
			cnt = token.tag.cont
			dst = self.getDst(token)
			log.info("%s, switching to destination %s, for context %s", self, dst, cnt)
			core.tokenCreator.setSwitch(self, cnt, dst)
		core.tokenCreator.switchToken(token, self)

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