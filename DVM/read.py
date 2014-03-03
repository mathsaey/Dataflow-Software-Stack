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

chunck = None

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
	opCode = int(arr[3])
	inputs = int(arr[4])
	op = natives.operations[opCode]

	return core.addOperationInstruction(op, inputs)

## 
# Defines the operation codes 
# and the functions to create them.
##
instructions = {
	'SI' : createSink,
	'PB' : createStart,
	'PE' : createStop,
	'CC' : createContextChange,
	'CR' : createContextRestore,
	'OP' : createOperation
}

##
# Parse an instruction declaration.
# Verify that it ended up in the correct chunck.
##
def parseInst(arr, stmt):
	code = arr[1]
	key = instructions[code](arr)
	if key != (chunck, int(arr[2])):
		log.error("Instruction %s added to memory with incorrect key %s", arr, key)
	else: log.info("Added instruction with key %s", key)

##
# Parse a chunck declaration.
#
# A chunck declaration has the form:
# `CHUNCK <idx>`
##
def parseChunck(arr, stmt):
	global chunck
	chunck = int(arr[1])

	log.info("Starting chunck: %d", chunck)

def parseLit(arr, stmt):
	inst = int(arr[1])
	port = int(arr[2])

	lit = stmt[stmt.find(arr[3]):]
	lit = evalLit(lit)

	log.info("Adding Literal: '%s' to c %d i %d p %d", 
		lit, chunck, inst, port)

	core.addLiteral((chunck, inst), port, lit)

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
	'CHUNCK' : parseChunck,
	'INST'   : parseInst,
	'LINK'   : parseLink,
	'LITR'   : parseLit
}

## 
# Parse a single DIS statement,
# the statement should not contain
# any comments.
##
def parseStmt(stmt):
	log.debug("Reading statement: '%s'", stmt)
	arr = stmt.split()
	key = arr[0]
	functions[key](arr, stmt)

## 
# Parse a dis string
##
def parse(str):
	for line in str.split('\n'):
		stmt = line.split('$')[0]
		if len(stmt) is not 0:
			parseStmt(stmt)
	log.info("Finished parsing, instruction memory: %s", core.memory.memory())

## Read the file at loc and parse it.
def parseFile(loc):
	file = open(loc, 'r')
	parse(file.read())