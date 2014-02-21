# memory.py
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
# \package dvm.memory
# \brief DVM instruction memory
#
# This module defines the instruction memory
# the instruction memory stores all the instructions in the program.
##

##
# The Instruction memory stores all of the 
# instructions in the program.
##
class InstructionMemory(object):

	def __init__(self):
		super(InstructionMemory, self).__init__()
		self.memory = {}
		self.matcherKey = 0
		self.standardKey = -1

	## Get a single instruction from memory
	def getInstruction(self, key):
		return self.memory[key]

	## 
	# Reserve a slot for an instruction that does
	# not require any context matching.
	##
	def reserveStandardSlot(self):
		key = self.standardKey
		self.standardKey -= 1
		return key

	##
	# Reserve a slot for an instruction that
	# requires context matching.
	##
	def reserveMatcherSlot(self):
		key = self.matcherKey
		self.matcherKey += 1
		return key

	##
	# Add an instruction to the memory.
	##
	def add(self, inst):
		key = None

		if inst.needsMatcher():
			key = self.reserveMatcherSlot()
		else:
			key = self.reserveStandardSlot()

		self.memory.update({key : inst})
		inst.setKey(key)
		return key

	##
	# Get an instruction from memory.
	##
	def get(self, key):
		return self.memory[key]

## Main instance of the instruction memory
__MEMORY__ = InstructionMemory()

## Get a reference to the instruction memory
def memory(): return __MEMORY__

## Delete all the contents of the instruction memory.
def reset(): 
	global __MEMORY__ 
	__MEMORY__= InstructionMemory()

## Get an instruction from the main memory
def get(key): return memory().get(key)

## Add an instruction to the main memory
def add(inst): return memory().add(inst)

## 
# See if an instruction needs to pass the matcher
# Instructions that require a context manager are stored
# in a separate part of the memory, so checking the key suffices.
#
# \param key
#		The key of the instruction 
# \return 
#		True if the instruction needs to be matched.
def needsMatcher(key): return key >= 0