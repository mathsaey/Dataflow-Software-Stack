# read.py
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
# \package read
# \brief DIS parser
#
# This module defines the function necessary to
# read DIS files.
##

import core
import natives

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

chunk = None

## Parse a literal string.
def evalLit(str):
	return eval(str)

## Create a sink.
def createSink(arr):
	return core.addSink()

## Create a stop instruction
def createStop(arr):
	return core.addStopInstruction()
##
# Create a start instruction.
#
# Creates a sink and adds the amount
# of incoming elements to the runtime.
##
def createStart(arr):
	core.setIn(int(arr[3]))
	return createSink(arr)

## Create a context change instruction.
def createContextChange(arr):
	dstChnk = int(arr[3])
	dstInst = int(arr[4])
	retChnk = int(arr[5])
	retInst = int(arr[6])
	return core.addContextChange((dstChnk, dstInst), (retChnk, retInst))

## Create a context restore
def createContextRestore(arr):
	return core.addContextRestore()

## Create an operation
def createOperation(arr):
	opCode = arr[3]
	inputs = int(arr[4])

	try:
		op = natives.operations[opCode]
		return core.addOperationInstruction(op, inputs)
	except KeyError:
		log.error("Invalid operation key: %s, using noOp instead.", opCode)
		return core.addOperationInstruction(natives.dvm_noOp, inputs)

## Create a switch instruction.
def createSwitch(arr):
	try:
		lst = [(int(arr[i]), int(arr[i+1])) for i in xrange(3, len(arr), 2)]
		return core.addSwitch(lst)
	except IndexError:
		log.error("Invalid destination list encountered: %s", arr)

## 
# Defines the operation codes 
# and the functions to create them.
##
instructions = {
	'SW' : createSwitch,
	'SI' : createSink,
	'PB' : createStart,
	'PE' : createStop,
	'CC' : createContextChange,
	'CR' : createContextRestore,
	'OP' : createOperation
}

##
# Parse an instruction declaration.
# Verify that it ended up in the correct chunk.
##
def parseInst(arr, stmt):
	code = arr[1]
	key = instructions[code](arr)
	if key != (chunk, int(arr[2])):
		log.error("Instruction %s added to memory with incorrect key %s", arr, key)
	else: log.info("Added instruction with key %s", key)

##
# Parse a chunk declaration.
#
# A chunk declaration has the form:
# `CHUNK <idx>`
##
def parseChunk(arr, stmt):
	global chunk
	chunk = int(arr[1])

	log.info("Starting chunk: %d", chunk)

##
# Parse a literal declarations.
#
# A literal declaration has the form:
# `LITR <instruction> <port> <= <value>`
##
def parseLit(arr, stmt):
	inst = int(arr[1])
	port = int(arr[2])

	litStart = stmt.find('<= ')

	if litStart == -1:
		log.error("Invalid literal declaraction: %s", stmt)
		return
	
	lit = stmt[litStart + 3:]
	lit = evalLit(lit)

	log.info("Adding Literal: '%s' to c %d i %d p %d", 
		lit, chunk, inst, port)

	core.addLiteral((chunk, inst), port, lit)

##
# Parse a link statement.
#
# A link statement has the form:
# `LINK <from> <to>` where from and
# to have the form:
# `<chunk> <instruction> <port>`
##
def parseLink(arr, stmt):
	srcChnk = int(arr[1])
	srcInst = int(arr[2])
	srcPort = int(arr[3])

	dstChnk = int(arr[4])
	dstInst = int(arr[5])
	dstPort = int(arr[6])

	log.info("Adding link from: c %d i %d p %d to: c %d i %d p %d", 
		srcChnk, srcInst, srcPort, dstChnk, dstInst, dstPort)

	core.addDestination(
		(srcChnk, srcInst), srcPort, 
		(dstChnk, dstInst), dstPort)

## Functions to parse the various statements.
functions = {
	'CHUNK' : parseChunk,
	'INST'   : parseInst,
	'LINK'   : parseLink,
	'LITR'   : parseLit
}

## Parse a single DIS line.
def parseLine(line):
	stmt = line.split('$')[0]
	stmt = stmt.strip()
	if len(stmt) is not 0:
		log.debug("Reading statement: '%s'", stmt)
		arr = stmt.split()
		key = arr[0]
		functions[key](arr, stmt)

## 
# Parse a dis string
##
def parse(str):
	for line in str.split('\n'):
		parseLine(line)
	log.info("Finished parsing, instruction memory: %s", core.memory.memory())
