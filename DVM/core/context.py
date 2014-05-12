# context.py
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
# \package core.context
# \brief DVM Contexts
# 
# This module defines contexts.
# Contexts allow us to add extra state to the
# runtime. They make it possible to have multiple inputs
# to the same instruction (e.g. multiple instances of the same function).
##

from math import sqrt, floor

##
# DVM Context
#
# A context is the part of a token tag.
# Contexts differentiate between various instances
# of a single part of the program.
# 
# For instance, when calling a function, DVM will create a new context
# shared by all the arguments to this function. Upon returning, the context
# will be used to find the destination of the function results.
#
# Internally, a context is a wrapper around a unique integer.
##
class Context(object):
	def __init__(self, core, key):
		super(Context,self).__init__()
		self.hash = self.hashPair(core, key)
		self.core = core

	def __str__(self):
		return "{" + str(self.hash) + "}"

	def __eq__(self, other):
		return self.hash == other.hash

	def __hash__(self):
		return self.hash

	## 
	# Generate a unique, integral identifier
	# for a pair of non-negative integers.
	#
	# \see http://szudzik.com/ElegantPairing.pdf
	# \see http://stackoverflow.com/a/13871379
	##
	def hashPair(self, a, b):
		if a >= b:
			return a ** 2 + a + b 
		else:
			return b ** 2 + a

	##
	# Unhashes the hash.
	#
	# \return a (prefix, key) pair
	# \see slide 8 of http://szudzik.com/ElegantPairing.pdf
	##
	def unhashPair(self):
		h = self.hash
		a = None
		b = None

		sqrtFloor   = floor(sqrt(h))
		sqrtFloorSq = sqrtFloor ** 2

		if (h - sqrtFloorSq) < sqrtFloor:
			a = h - sqrtFloorSq
			b = sqrtFloor
		else:
			a = sqrtFloor
			b = h - sqrtFloorSq - sqrtFloor

		return (a,b)

##
# Context creator
#
# Allows the generation of new contexts.
#
# A context creater has a unique prefix.
# Having this prefix allows us to have multiple context 
# creators that generate unique contexts without synchronizing.
##
class ContextCreator(object):
	def __init__(self, core):
		self.core = core.identifier
		self.current = 0
		self.available = []

	def get(self):
		#if self.available:
		#	return self.available.pop()
		#else:
		res = self.current
		self.current += 1
		return Context(self.core, res)

	def restore(self, context):
		self.available.append(context)