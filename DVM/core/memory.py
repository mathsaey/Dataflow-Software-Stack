# memory.py
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
# \package core.memory
# \brief DVM instruction memory
#
# This module defines the instruction memory
# the instruction memory stores all the instructions in the program.
##

##
# The Instruction memory stores all of the 
# instructions in the program.
#
# An instruction memory is divided into chuncks.
# each of these chuncks stores instructions with 
# certain properties. The exact properties are
# determined by the outside world.
##
class InstructionMemory(object):

	def __init__(self, chuncks):
		super(InstructionMemory, self).__init__()
		self.memory = [[] for i in xrange(0, chuncks)]

	##
	# Add an instruction to the memory.
	##
	def add(self, inst, chunck):
		key = (chunck, len(self.memory[chunck]))
		lst = self.memory[chunck]
		lst.append(inst)
		inst.setKey(key)
		return key

	##
	# Get an instruction from memory.
	##
	def get(self, key):
		return self.memory[key[0]][key[1]]

## Main instance of the instruction memory
__MEMORY__ = InstructionMemory(2)

## Get a reference to the instruction memory
def memory(): return __MEMORY__

## Delete all the contents of the instruction memory.
def reset(): 
	global __MEMORY__ 
	__MEMORY__= InstructionMemory()

## Get an instruction from the main memory
def get(key): return memory().get(key)

## 
# See if an instruction needs to pass the matcher
# Instructions that require a context manager are stored
# in a separate part of the memory, so checking the key suffices.
#
# \param key
#		The key of the instruction 
# \return 
#		True if the instruction needs to be matched.
def needsMatcher(key): return key[0] is 0

## 
# Add an instruction to the main memory.
#
# This function has to determine the chunck
# of memory that the instruction will use.
##
def add(inst): 
	chunck = None
	if inst.needsMatcher(): chunck = 0
	else: chunck = 1
	return memory().add(inst, chunck)
