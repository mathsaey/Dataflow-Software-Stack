# tokenCreator.py
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
# \package core.tokenCreator
# \brief DVM token creator
#
# This module defines the token creator.
##

import token

##
# DVM Token creator.
#
# The token creator is responsible for
# wrapping results of instructions in tokens.
##
class TokenCreator(object):
	def __init__(self, core):
		super(TokenCreator, self).__init__()
		self.core = core

		self.contextMap = {}
		self.restoreMap = {}

		self.tokenStore = {}
		self.switchMap  = {}

	## 
	# Create a simple token, with a known destination.
	# The token will remain on the current core.
	##
	def simpleToken(self, datum, toInst, toPort, context):
		tag = token.Tag(self.core.identifier, toInst, toPort, context)
		tok = token.Token(datum, tag)
 		self.core.add(tok)

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
 	def switchToken(self, token, inst):
 		key = (inst.key, token.tag.cont)

 		if key in self.switchMap:
 			dst = self.switchMap[key]
 			token.tag.inst = dst
 			self.core.add(token)
 		else:
 			if key in self.tokenStore:
 				lst = self.tokenStore[key]
 				lst.append(token)
 			else:
 				self.tokenStore.update({key : [token]})

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
 	def setSwitch(self, inst, cont, dst):
 		key = (inst.key, cont)

 		self.switchMap.update({key : dst})

 		if key in self.tokenStore:
 			lst = self.tokenStore[key]
 			del self.tokenStore[key]

 			for token in lst:
 				token.tag.inst = dst
 				self.core.add(token)

 	##
 	# Create a new context for a token.
 	# And send it. This should only be called
 	# if we have not sent any token for this context.
 	#
 	# This method will also send any literals that belong
 	# to the call node.
 	#
 	# \param tok
 	#		The token to modify and send.
 	# \param inst
 	#		The instruction that started the context change.
 	# \param dest
 	#		The new destination of the token.
 	##
 	def createNewContext(self, tok, inst, dest):
 		core = tok.tag.core
 		cont = tok.tag.cont
 		key  = (inst.key, cont)

 		new = self.core.contextCreator.get()
		self.contextMap.update({key : new})
		self.restoreMap.update({new : (cont, inst.retnSink)})

		# Add the value
		tok.tag.cont = new
		tok.tag.inst = dest
		self.core.add(tok)

		# Add the literals of the call
		for key in inst.getLiterals():
			val = inst.getLiterals()[key]
			tag = token.Tag(core, dest, key, new)
			tok = token.Token(val, tag)
			self.core.add(tok)

 	##
 	# Change the context of a token.
 	# Only use this if the context has already
 	# been created.
 	#
 	# \param token 
 	#		The token to send.
 	# \param key
 	#		The instruction, context pair of the token.
 	# \param dest
	#		The destination of the token.
 	##
 	def sendToOldContext(self, token, key, dest):
 		cont = self.contextMap[key]
 		token.tag.cont = cont
 		token.tag.inst = dest
 		self.core.add(token)

	## 
	# Change the context of a token.
	# This will bind the context of this token to a 
	# certain return instruction.
	#
	# The runtime may decide to send these tokens
	# to a different runtime core.
	#
	# Multiple tokens that are sent from the same instruction with the same 
	# context will receive the same context.
	#
	# \param token
	#		The token to modify. The destination port of this token
	#		will remain unchanged.
	# \param inst
	#		The instruction that called the contextchange.
	#		this has to be a contextChange instruction.
	#
	# \see restoreContext
	##
	def changeContext(self, token, inst):
		dest = inst.destSink
		cont = token.tag.cont
		key  = (inst.key, cont)

		if key not in self.contextMap:
			self.createNewContext(token, inst, dest)
		else:
			self.sendToOldContext(token, key, dest)

	##
	# Restore the old context of a token.
	# 
	# In order to do this, we simply look up the previous context 
	# and the return instructions that are bound to this context.
	##
	def restoreContext(self, token):
		cont = token.tag.cont
		pair = self.restoreMap[cont]

		token.tag.cont = pair[0]
		token.tag.inst = pair[1]
		self.core.add(token)

	##
	# Create a stop token.
	#
	# \param tok
	#		The token to convert to
	#		a stop token.
	##
	def stopToken(self, tok):
		tok.tag = token.StopTag()
		self.core.add(tok)