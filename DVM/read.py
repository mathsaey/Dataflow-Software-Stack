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

import logging
log = logging.getLogger(__name__)

chunck = None

## Create a sink.
def createSink(arr):
	return core.addSink()

def createContextChange(arr):
	dstChnk = int(arr[3])
	dstInst = int(arr[4])
	retChnk = int(arr[5])
	retInst = int(arr[6])
	return core.addContextChange((dstChnk, dstInst), (retChnk, retInst))

## Create a context restore
def createContextRestore(arr):
	return core.addContextRestore()

def tOP(a,b):
	return a + b

def createOperation(arr):
	#opCode = int(arr[3])
	inputs = int(arr[4])

	return core.addOperationInstruction(tOP, inputs)

instructions = {
	'SI' : createSink,
	'PB' : createSink,
	'PE' : createSink,
	'CC' : createContextChange,
	'CR' : createContextRestore,
	'OP' : createOperation
}

##
# Parse an instruction declaration.
# Verify that it ended up in the correct chunck.
##
def parseInst(arr):
	code = arr[1]
	key = instructions[code](arr)
	if key != (chunck, int(arr[2])):
		log.critical("Instruction %s added to memory with incorrect key %s", arr, key)

##
# Parse a chunck declaration.
#
# A chunck declaration has the form:
# `CHUNCK <idx>`
##
def parseChunck(arr):
	global chunck
	chunck = int(arr[1])

##
# Parse a link statement.
#
# A link statement has the form:
# `LINK <from> <to>` where from and
# to have the form:
# `<chunk> <instruction> <port>`
##
def parseLink(arr):
	srcChnk = int(arr[1])
	srcInst = int(arr[2])
	srcPort = int(arr[3])

	dstChnk = int(arr[4])
	dstInst = int(arr[5])
	dstPort = int(arr[6])

	core.addDestination(
		(srcChnk, srcInst), srcPort, 
		(dstChnk, dstInst), dstPort)

## Functions to parse the various statements.
functions = {
	'CHUNCK' : parseChunck,
	'INST'   : parseInst,
	'LINK'   : parseLink,
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
	functions[key](arr)

## 
# Parse a dis string
##
def parse(str):
	for line in str.split('\n'):
		stmt = line.split('$')[0]
		if len(stmt) is not 0:
			parseStmt(stmt)

## Read the file at loc and parse it.
def parseFile(loc):
	file = open(loc, 'r')
	parse(file.read())