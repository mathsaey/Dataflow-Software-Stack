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

import sys
import core
import user
import natives

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

chunk = None

# ----------- #
# Convenience #
# ----------- #

## Parse a value string.
def parseValue(str):
	try:
		return eval(str)
	except SyntaxError, e:
		log.error("Invalid literal syntax: %s", e.text)
		sys.exit(user.EXIT_INPUT)

##
# Extract the value of a statement.
#
# The value of a statement is found after the statement,
# and seperated from the statement by a `<=` and a space.
##
def extractValue(stmt):
	valStart = stmt.find('<= ')

	if valStart == -1:
		log.error("Missing value in statement: %s", stmt)
		return

	val = stmt[valStart + 3:]
	return parseValue(val)

## 
# Get a list of instruction addresses
# from the array, starting at idx start.
##
def getInstructionList(arr, start):
	try:
		return [(int(arr[i]), int(arr[i+1])) for i in xrange(start, len(arr), 2)]
	except IndexError:
		log.error("Invalid destination list encountered: %s", arr)
		return []

# ------------ #
# Instructions #
# ------------ #

## Create a sink.
def createSink(arr, stmt):
	return core.addSink()

## Create a constant.
def createConstant(arr, stmt):
	return core.addConstant(extractValue(stmt))

## Create a stop instruction
def createStop(arr, stmt):
	return core.addStopInstruction()
##
# Create a start instruction.
#
# Creates a sink and adds the amount
# of incoming elements to the runtime.
##
def createStart(arr, stmt):
	core.setIn(int(arr[3]))
	return createSink(arr, stmt)

## Create a context change instruction.
def createContextChange(arr, stmt):
	changes = int(arr[3])
	returns = int(arr[4])
	dstChnk = int(arr[5])
	dstInst = int(arr[6])
	retChnk = int(arr[7])
	retInst = int(arr[8])
	return core.addContextChange(changes, returns, (dstChnk, dstInst), (retChnk, retInst))

## Create a context map function
def createSplit(arr, stmt):
	changes  = int(arr[3])
	restores = int(arr[4])
	destChnk = int(arr[5])
	destInst = int(arr[6])
	retnChnk = int(arr[7])
	retnInst = int(arr[8])
	mergeLst = getInstructionList(arr, 9)
	return core.addSplit(changes, restores, (destChnk, destInst), (retnChnk, retnInst), mergeLst)

## Create a merge instruction.
def createMerge(arr, stmt):
	return core.addMerge()

## Create a context restore
def createContextRestore(arr, stmt):
	return core.addContextRestore()

## Create an operation
def createOperation(arr, stmt):
	opCode = arr[3]
	inputs = int(arr[4])

	try:
		op = natives.operations[opCode]
		return core.addOperationInstruction(op, inputs)
	except KeyError:
		log.error("Invalid operation key: %s, using noOp instead.", opCode)
		return core.addOperationInstruction(natives.dvm_noOp, inputs)

## Create a switch instruction.
def createSwitch(arr, stmt):
	return core.addSwitch(getInstructionList(arr, 3))

## 
# Defines the operation codes 
# and the functions to create them.
##
instructions = {
	'SWI' : createSwitch,
	'SNK' : createSink,
	'BGN' : createStart,
	'STP' : createStop,
	'SPL' : createSplit,
	'MRG' : createMerge,
	'CHN' : createContextChange,
	'RST' : createContextRestore,
	'OPR' : createOperation,
	'CNS' : createConstant
}

# ---------- #
# Statements #
# ---------- #

##
# Parse an instruction declaration.
# Verify that it ended up in the correct chunk.
##
def parseInst(arr, stmt):
	code = arr[1]
	key = instructions[code](arr, stmt)
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

	lit = extractValue(stmt)

	log.info("Adding Literal: '%s' to c %d i %d p %d", 
		lit, chunk, inst, port)

	core.addLiteral((chunk, inst), port, lit)

##
# Parse a link statement.
#
# A link statement has the form:
# `LINK <from> -> <to>` where from and
# to have the form:
# `<chunk> <instruction> <port>`
##
def parseLink(arr, stmt):
	srcChnk = int(arr[1])
	srcInst = int(arr[2])
	srcPort = int(arr[3])

	dstChnk = int(arr[5])
	dstInst = int(arr[6])
	dstPort = int(arr[7])

	log.info("Adding link from: c %d i %d p %d to: c %d i %d p %d", 
		srcChnk, srcInst, srcPort, dstChnk, dstInst, dstPort)

	core.addDestination(
		(srcChnk, srcInst), srcPort, 
		(dstChnk, dstInst), dstPort)

##
# Parse a trivial statement.
#
# A trivial statement has the form:
# `TRIV <= <value>`
##
def parseTriv(arr, stmt):
	val = extractValue(stmt)
	core.addTrivial(val)

# ------- #
# General #
# ------- #

## Functions to parse the various statements.
functions = {
	'CHUNK' : parseChunk,
	'INST'   : parseInst,
	'LINK'   : parseLink,
	'LITR'   : parseLit,
	'TRIV'   : parseTriv
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
