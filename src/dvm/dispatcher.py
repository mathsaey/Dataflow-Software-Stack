# dispatcher.py
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
# \file dvm/dispatcher.py
# \namespace dvm.dispatcher
# \brief DVM token dispatcher
#
# This module defines the token dispatcher.
# The token dispatcher is responsible for deciding how to
# handle received tokens.
##

##
# Token Dispatcher.
#
# The token dispatcher is responsible
# for processing the incoming tokens and deciding how
# to handle them.
##
class TokenDispatcher(object):
	def __init__(self, core):
		super(TokenDispatcher, self).__init__()
		self.core = core

	##
	# See if the token comes from the same prefix.
	#
	# \param tag
	#		The tag of the token to check.
	# 
	# \return
	#		True if the token is from the same core.
	##
	def checkPrefix(self, tag):
		return tag.core == self.core.prefix

	##
	# See if a given token is a special token.
	#
	# \param tag
	#		The tag of the token to check.
	# 
	# \return
	#		True if the token is special
	##	
	def checkSpecial(self, tag):
		return tag.isSpecial()

	##
	# Add a token to a different core.
	##
	def sendToCore(self, token):
		c = self.core.cores[token.tag.prefix]
		c.accept(token)

	##
	# Send a stop token to every core in the system.
	##
	def sendStop(self, token):
		for core in self.core.cores:
			core.accept(token)

	def processToken(self, token):
		inst = token.tag.inst
		if inst < 0:
			self.addInstruction(inst, token)
		else:
			self.addToContext(token)
