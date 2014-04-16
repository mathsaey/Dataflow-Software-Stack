# tokenizer.py
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
# \package core.tokenizer
# \brief DVM token creator
#
# This module defines the more practical part of
# the instruction execution. It is responsible for generating
# new tokens for instructions. It's also responsible for managing
# the contexts and destinations of these tokens when the semantics of
# the instruction call for it.
##

from token import Tag, StopTag, Token

import logging
log = logging.getLogger(__name__)

##
# DVM Token creator.
#
# The token creator is responsible for
# wrapping results of instructions in tokens.
##
class Tokenizer(object):
	def __init__(self, core):
		super(Tokenizer, self).__init__()
		self.core = core

		self.switcher = Switcher(self)
		self.contexts = ContextManager(self)

		self.contextMap = {}
		self.restoreMap = {}

	##
	# Add a token to the runtime.
	# Use instead of directly using the core, so that
	# we have a central point for redirecting the token
	# to a different core.
	##
	def add(self, token):
		self.core.add(token)

	## Create a simple token, with a known destination.
	def simple(self, datum, toInst, toPort, context):
		tag = Tag(self.core.identifier, toInst, toPort, context)
		tok = Token(datum, tag)
 		self.add(tok)

	##
	# Create a stop token.
	#
	# \param tok
	#		The token to convert to
	#		a stop token.
	##
	def stopToken(self, tok):
		tok.tag = StopTag()
		self.add(tok)

##
# Context Manager
#
# The Context manager is reponsible for changing
# and restoring the context of tokens.
##
class ContextManager(object):
	def __init__(self, tokenizer):
		super(ContextManager, self).__init__()
		self.tokenizer = tokenizer

		##
		# Stores the contexts that have already been
		# created. This is needed incase multiple tokens
		# need to be sent to the same context (e.g. function call)
		##
		self.contextMap = {}

		##
		# Stores the old context and the destination
		# for restoring contexts.
		##
		self.restoreMap = {}

	## 
	# Send a token to a different context.
	# Create this context first if it does not exist yet.
	# Further tokens from the same source (instruction, context) pair
	# will be sent to the same context.
	#
	# \param token
	#		The token to change and send.
	# \param inst
	#		The instruction that wants to change the token.
	# \param dest
	#		The new destination of the token.
	# \param retInst
	#		The instance to send the token to
	#		when restoring the context.
	# \param binds
	#		The amount of tokens that will 
	#		be bound to the context.
	# \param restores
	#		The amount of tokens the context will 
	#		produce before being deleted.
	##
	def bindMany(self, token, inst, dest, retInst, binds, restores):
		key = (inst.key, token.tag.cont)
		cont = None

		if key in self.contextMap:
			pair = self.contextMap[key]
			cont = pair[0]
			pair[1] -= 1

			if pair[1] <= 0:
				del self.contextMap[key]

		else:
			cont = self.bind(retInst, None, token.tag.cont, restores)
			self.contextMap.update({key : [cont, binds - 1]})

			for key in inst.getLiterals():
				val = inst.getLiterals()[key]
				tag = Tag(token.tag.core, dest, key, cont)
				tok = Token(val, tag)
				self.tokenizer.add(tok)

		token.tag.cont = cont
		token.tag.inst = dest
		self.tokenizer.add(token)

 	##
 	# Bind a new context to a given context and destination.
 	# When a token with the new context encounters a context restore
 	# operation, it will be bound to the old context, and new instruction.
 	#
 	# \param destination
 	#		The instruction to bind to the context.
 	# \param port
 	#		The port to bind to the context.
 	#		None if the port should not change.
 	# \param context
 	#		The context to restore.
 	# \param restores
 	#		The amount of tokens the context will produce.
 	##
 	def bind(self, destInst, destPort, context, restores):
 		cont = self.tokenizer.core.contextCreator.get()
 		self.restoreMap.update({cont : [destInst, destPort, context, restores]})
 		return cont

	##
	# Restore a token.
	#
	# In order to do this, we simply change the
	# destination and context of the token to those
	# found in the restoremap.
	##
	def restore(self, token):
		cont = token.tag.cont
		pair = self.restoreMap[cont]

		pair[3] -= 1

		if pair[3] <= 0:
			del self.restoreMap[cont]

		token.tag.inst = pair[0]
		token.tag.cont = pair[2]
		if pair[1] is not None:
			token.tag.port = pair[1]
		self.tokenizer.add(token)

##
# Token Switcher
#
# The token switcher is responsible for storing and 
# sending tokens for a switch instruction.
##
class Switcher(object):
	def __init__(self, tokenizer):
		super(Switcher, self).__init__()
		self.tokenizer = tokenizer

		##
		# Store the tokens that
		# have not received a destination
		##
		self.storage = {}

		##
		# Store the known destination
		# of certain switch instructions.
		##
		self.destinations = {}

	##
	# Send a token to it's destination.
	# Assumes the destination is present in the
	# destination map.
	#
	# \param key
	#		The key of the switch.
	# \param token
	#		The token to send.
	##
	def send(self, key, token):
		dst = self.destinations[key]
		token.tag.inst = dst
		self.tokenizer.add(token)
	## 
	# Store a token.
	#
	# \param key
	#		The key of the switch.
	# \param token
	#		The token to store.
	##
	def store(self, key, token):
		if key in self.storage:
			lst = self.storage[key]
			lst.append(token)
		else:
			self.storage.update({key : [token]})

	##
	# Send all the stored tokens
	# that were waiting for a switch to be set.
	#
	# \param key
	#		The key of the switch that was set.
	#		And the context for which this was set.
	# \param dst
	#		The destination for the tokens.
	##
	def sendStored(self, key, dst):
 		if key in self.storage:
 			lst = self.storage[key]
 			del self.storage[key]

 			for token in lst:
 				token.tag.inst = dst
 				self.tokenizer.add(token)
	##
 	# Set the destination of tokens for
 	# a given (switch instruction, context) pair.
 	# This will also release all the tokens that are
 	# stored for this context.
 	#
 	# \param inst
 	#		The instruction that sent the switch.
 	# \param cont
 	#		The context that received the setSwitch
 	# \param dst
 	#		The destination of the tokens of the switch.
 	##	
 	def set(self, inst, cont, dst):
 		key = (inst.key, cont)
 		self.destinations.update({key : dst})
 		self.sendStored(key, dst)

 	##
 	# Send a token to the destination of a SwitchInstruction.
 	# Store the token if the destination is currently unknown.
 	# Only the instruction address of the token tag is modified.
 	#
 	# \param token
 	#		The token to switch
 	# \param inst
 	#		The instruction that sent the token.
 	##
 	def switch(self, token, inst):
 		key = (inst.key, token.tag.cont)

 		if key in self.destinations:
 			self.send(key, token)
 		else:
 			self.store(key, token)