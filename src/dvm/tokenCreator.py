# tokenCreator.py
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
# \file dvm/tokenCreator.py
# \namespace dvm.tokenCreator
# \brief DVM token creator
#
# This module defines the token creator.
##

import token
import multiprocessing

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
		self.lock = multiprocessing.Lock()

		self.contextMap = {}
		self.restoreMap = {}

	## Create a simple token, with a known destination.
	def simpleToken(self, datum, toInst, toPort, context):
		tag = token.Tag(toInst, toPort, context)
		tok = token.Token(datum, tag)
		self.core.dispatcher.add(tok)

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
	# \param toInst
	#		The instruction that will be the new destination of this
	#		token.
	# \param retInst
	#		The return instruction that will be bound to the new context.
	#
	# \see restoreContext
	##
	def changeContext(self, token, inst, toInst, retInst):
		cont = token.tag.cont
		key  = (inst, cont)
		new  = None

		if key not in self.contextMap:
			new = self.core.contextCreator.get()
			self.contextMap.update({key : new})
			self.restoreMap.update({new : (cont, retInst)})
		else:
			new = self.contextMap[key]

		token.tag.cont = new
		token.tag.inst = toInst
		self.core.dispatcher.add(token)

	##
	# Restore the old context of a token.
	# 
	# In order to do this, we simply look up the previous context 
	# and the return instruction that are bound to this context.
	##
	def restoreContext(self, token):
		cont = token.tag.cont
		pair = self.restoreMap[cont]

		token.tag.cont = pair[0]
		token.tag.inst = pair[1]
		self.core.dispatcher.add(token)


