# context.py
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
# \file dvm/context.py
# \namespace dvm.context
# \brief DVM Contexts
# 
# This module defines contexts.
# Contexts allow us to add extra state to the
# runtime. They make it possible to have multiple inputs
# to the same instruction (e.g. multiple instances of the same function).
##

import multiprocessing

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
# Internally, a context is a simple unique piece of data.
##
class Context(object):
	def __init__(self, key):
		super(Context,self).__init__()
		self.key = key

	def __str__(self):
		return "Context: " + str(self.key)

	def __eq__(self, other):
		return other.key == self.key

	def __hash__(self):
		return self.key

##
# Context creator
#
# Allows the generation of new contexts.
# For efficieny reasons, it's possible to return
# old contexts to the creator, this allows us to reclycle
# contexts instead of always creating new ones.
##
class ContextCreator(object):
	def __init__(self):
		self.current = 0
		self.free = []
		self.lock = multiprocessing.Lock()

	def get(self):
		with self.lock:
			if self.free:
				res = self.free[0]
				self.free = self.free[1:]
				return res
			else:
				res = self.current
				self.current += 1
				return Context(res)

	def release(self, cont):
		with self.lock:
			self.free = [cont] + self.free
