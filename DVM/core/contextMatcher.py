# contextMatcher.py
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
# \package core.contextMatcher
# \brief DVM context matcher
# 
# This module defines the DVM context matcher.
##

import logging
log = logging.getLogger(__name__)

##
# DVM Context matcher.
#
# The matcher is responsible for gathering inputs 
# to the same instruction based on their contexts.
# The matcher should forward these tokens to the scheduler once
# that all of the inputs for a given context are available.
#
# The matcher utilizes <i>(instruction, context)</i> pairs as **keys**
##
class ContextMatcher(object):

	##
	# Initialize a context matcher.
	#
	# \param core
	#		The runtime core that this matcher
	#		is a part of.
	##
	def __init__(self, core):
		super(ContextMatcher, self).__init__()

		## Dictionary that contains the tokens for all the keys
		self.tokens = {}

		## Reference to the DVM::Core
		self.core = core

	##
	# Dynamically define the amount of inputs of a 
	# (instruction, context) pair. This allows us to
	# dynamically join arrays of unknown length at runtime.
	##
	def prepareKey(self, key, inputs):
		self.tokens.update({key : ([None] * inputs, 0, inputs)})

	##
	# See if a given key is already a part of the 
	# tokens we are matching.
	# 
	# Create an array to match these tokens if it's not.
	#
	# \param key
	#		The key to check
	##
	def checkKey(self, key):
		if key not in self.tokens:
			inst = self.core.memory.get(key[0])
			arr = [None] * inst.totalinputs
			inp = inst.realInputs
			self.tokens.update({key : [arr, 0, inp]})

	##
	# Update the token array for a key
	# This method assumes that there is an array for the
	# given key.
	#
	# \param key
	#		The key to find the array we want to update.
	# \param port
	#		The destination port of the token we want to add.
	# \param token
	#		The token we want to add.
	##
	def updateKeyArr(self, key, port, token):
		pair = self.tokens[key]
		if not pair[0][port]:
			pair[0][port] = token
			pair[1] += 1
		else:
			log.warning("Duplicate token received!")

	##
	# See if all the input tokens are present
	# for a given key.
	#
	# \param key
	#		The key to check
	# 
	# \return 
	#		True if all the input tokens are present for key.
	##
	def isKeyReady(self, key):
		pair = self.tokens[key]
		return pair[1] == pair[2]

	##
	# Add the tokens for key to the scheduler.
	##
	def executeKey(self, key):
		log.info("Executing key: (%s, %s)", key[0], key[1])
		arr = self.tokens[key][0]
		del self.tokens[key]
		self.core.scheduler.schedule(key[0], arr)

	## 
	# Add a token to the matcher
	# 
	# This method can be seen as the main method of the
	# matcher as it utilizes all the other methods to define
	# the behaviour that the matcher will use when a token is added.
	#
	# \param token
	#		the token to add.
	##
	def add(self, token):
		log.info("Adding token: %s", token)

		tag  = token.tag                  
		inst = tag.inst                   
		cont = tag.cont                   
		port = tag.port                   
		key  = (inst, cont)

		self.checkKey(key)
		self.updateKeyArr(key, port, token)

		if self.isKeyReady(key):
			self.executeKey(key)
