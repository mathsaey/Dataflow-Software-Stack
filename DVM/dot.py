# dot.py
# Mathijs Saey
# DVM

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentat ion files (the "Software"), to deal
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
# \package dot
# \brief dot generator
#
# This module defines a tool that allows us 
# to generate graphs from the instruction memory.
##

import StringIO
import subprocess
import core.memory
import core.instruction

import logging
log = logging.getLogger(__name__)


# ------- #
# General #
# ------- #

## Generate a unique idea for a chunk/key pair.
def generateIdentifier(chunk, key):
	if chunk >= key: return chunk ** 2 + chunk + key 
	else: return key ** 2 + chunk

## Generate a unique identifier for an instruction.
def generateInstIdentifier(inst):
	return generateIdentifier(inst.key[0], inst.key[1])

## Generate a unique identifier for a chunk, key pair.
def generateTupleIdentifier(tup):
	return generateIdentifier(tup[0], tup[1])

# ------------ #
# Instructions #
# ------------ #

def processSink(inst):
	shape = "shape = record"
	label = "|".join(["<%d>" % i for i in xrange(max(inst.destinations.keys()) + 1)])
	label = "{Sink: %s|{%s}}" % (inst.key[1], label)
	label = 'label = "%s"' % label
	return "%s, %s" % (shape, label)

def processOp(inst):
	shape = "shape = Mrecord"

	lits = [str(l) if l is not None else "" for l in inst.litLst]
	inputs = "|".join(["<%d> %s" % (i, lits[i]) for i in xrange(0, inst.totalinputs)])

	name = inst.operation.__name__
	label = 'label = "{{%s} | %s}"' % (inputs, name)

	return "%s, %s" % (shape, label)

def processConst(inst):
	return "shape = circle, label = %s" % inst.value

def processSplit(inst):
	return 'shape = ellipse, label = "Split: %s"' % inst.destSink[1]

def processContChange(inst):
	return 'shape = ellipse, label = "Send: %s"' % inst.destSink[1]

def processContRestore(inst):
	return 'shape = ellipse, style = dashed, label = ""'

def processSwitch(inst):
	return "shape = diamond, label = Switch"

def processStop(inst):
	return "shape = point"

attributes = {
	core.instruction.OperationInstruction : processOp,
	core.instruction.Constant             : processConst,
	core.instruction.Sink                 : processSink,
	core.instruction.Split                : processSplit,
	core.instruction.ContextChange        : processContChange,
	core.instruction.ContextRestore       : processContRestore,
	core.instruction.Switch               : processSwitch,
	core.instruction.StopInstruction      : processStop
}

def getAttributes(inst):
	return attributes[type(inst)](inst)
	
def addInst(buffer, inst):
	key = generateInstIdentifier(inst)
	att = getAttributes(inst)
	buffer.write("%s [%s];\n" % (key, att))

# ----- #
# Links #
# ----- #

def destMapLinks(buffer, inst):
	key = generateInstIdentifier(inst)
	for src in inst.destinations:
		for dst in inst.destinations[src]:
			dstKey = generateTupleIdentifier(dst[0])
			dstPrt = dst[1]
			buffer.write("%d : %d -> %d : %d ; \n" % (key, src, dstKey, dstPrt))

def destListLinks(buffer, inst):
	key = generateInstIdentifier(inst)
	for dst in inst.destinations:
		dstKey = generateTupleIdentifier(dst[0])
		dstPrt = dst[1]
		buffer.write("%d -> %d : %d ; \n" % (key, dstKey, dstPrt))

def addContextChangeLinks(buffer, inst):
	srcKey = generateInstIdentifier(inst)
	retKey = generateTupleIdentifier(inst.retnSink)
	buffer.write("%s -> %s ; \n" % (srcKey, retKey))

def addContextMapLinks(buffer, inst):
	srcKey = generateInstIdentifier(inst)
	retKey = generateTupleIdentifier(inst.mergeOp)
	buffer.write("%s -> %s ; \n" % (srcKey, retKey))

def addSwitchLinks(buffer, inst):
	for dst in inst.dstLst:
		srcKey = generateInstIdentifier(inst)
		dstKey = generateTupleIdentifier(dst)
		buffer.write("%s -> %s [style = dashed]; \n" % (srcKey, dstKey))

def addLinks(buffer, inst):
	# Soft links
	if isinstance(inst, core.instruction.DestinationMap):
		destMapLinks(buffer, inst)
	elif isinstance(inst, core.instruction.DestinationList):
		destListLinks(buffer, inst)

	# Hard links
	if isinstance(inst, core.instruction.ContextChange):
		addContextChangeLinks(buffer, inst)
	elif isinstance(inst, core.instruction.ContextMap):
		addContextMapLinks(buffer, inst)
	elif isinstance(inst, core.instruction.Switch):
		addSwitchLinks(buffer, inst)

# ----- #
# Other #
# ----- #

def dotHeader(buffer):
	buffer.write("digraph IGR {\n")

def dotFooter(buffer):
	buffer.write("}")

# ------------- #
# Parsing Logic #
# ------------- #

## Generate a dot string from the instruction memory.
def dotString():
	buffer = StringIO.StringIO()

	dotHeader(buffer)
	for mem in core.memory.memory().memory:
		for inst in mem:
			addInst(buffer, inst)
			addLinks(buffer, inst)
	dotFooter(buffer)

	str = buffer.getvalue()
	buffer.close()
	return str

## Write the dot string to a file.
def dotFile(path):
	f = open(path, 'w')
	f.write(dotString())
	f.close()

##
# Convert the instruction memory to dot,
# save it and run dot on this file.
#
# This function should be call with keyword arguments.
# The default arguments will cause the following behaviour:
# 		* dot is assumed to be in your PATH.
#		* the dot file will be saved in dis.dot
#		* the output will be in png format.
#		* dot will decide where to store the output.
#			With the default settings this would be in dis.dot.png
#
# \param dotpath
#		The path of the dot executable, in case it's not in your PATH
# \param path
#		The location where the dot file will be stored.
# \param format
#		The output format of the graph dot creates from the dot file.
# \param output
#		The location where we store the output of dot.
#		Leaving this blank will pass the -O option.
#		The -O option let's dot choose the path.
# \param other
#		Any other options you want to pass to doth.
#		These options should be passed as a list of strings.
##
def dot(
	dotpath = "dot",
	path = "dis.dot", 
	format = "png", 
	output = "", 
	other = [], 
	):

	dotFile(path)

	format = "-T" + format

	if output: output = "-o" + output
	else: output = "-O"

	try:
		subprocess.check_call([dotpath, format, path, output, '-q'] + other)
	except subprocess.CalledProcessError, e:
		log.error("Dot returned with exit code %d", e.returncode)
	except OSError:
		log.error("Dot executable not found")

