# __init__.py
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
# \package dvm
# \brief Dataflow Virtual Machine
# 
# This is the core of DVM. It defines the underlying instructions,
# tokens, and execution model
#
# The top level namespace of DVM declares some convenience functions
# to easily create the program.
##

import instruction
import runtime
import memory

##
# Create an instruction and add it to memory.
# 
# \param constructor
#		The instruction constructor
# \param argLst
#		The arguments to pass to the constructor.
#		The exact sructure of this list depends on the
#		instruction type.
#
# \return 
#		The key of the newly added instruction.
##
def _addInstruction(constructor, argLst = []):
	inst = constructor(*argLst)
	return memory.add(inst)

## 
# Add an operation instruction.
#
# \param op
#		The operation of this instruction.
# \param inputs
#		The amount of inputs this instruction
#		will accept.
#
# \return
#		The key of the operation instruction.
##
def addOperationInstruction(op, inputs):
	return _addInstruction(
		instruction.OperationInstruction,
		[op, inputs])

##
# Add a sink instruction.
#
# \return
#		The key of the sink instruction.
##
def addSink():
	return _addInstruction(instruction.Sink)

##
# Add a context change instruction.
#
# \param destSink
#		The destination of the token after
#		the context change.
# \param retSink
#		The destination of the token
#		after the context restore.
#
# \return 
#		The key of the context change instruction.
##
def addContextChange(destSink, retSink):
	return _addInstruction(
		instruction.ContextChange,
		[destSink, retSink])

##
# Add a context restore instruction.
#
# \return 
#		The key of the context restore instruction.
##
def addContextRestore():
	return _addInstruction(instruction.ContextRestore)

##
# Add a stop instruction.
#
# \return
#		The key of the stop instruction.
##
def addStopInstruction():
	return _addInstruction(instruction.StopInstruction)

##
# Add a destination to a given instruction.
#
# This only works on instruction::OperationInstruction 
# and on instruction::Sink
#
# \param srcKey
#		The key of the from instruction.
# \param scrPort
#		The index of the from port.
# \param dstKey
#		The key of the destination instruction.
# \param dstPort
#		The index of the destination port.
##
def addDestination(srcKey, srcPort, dstKey, dstPort):
	inst = memory.get(srcKey)
	inst.addDestination(srcPort, dstKey, dstPort)

##
# Start program execution
#
# \see runtime::start()
##
def start(cores = 1): runtime.start(cores)
