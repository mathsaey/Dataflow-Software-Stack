# literals.py
# Mathijs Saey
# DISc

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
# \package backEnd.DVM.literals
# \brief IGR Literal removal
# 
# This module defines a few traversals
# that remove literals from the IGR where
# possible.
##

import dvm
import dis
import IGR.node
import converter
import graphConverter


import logging
log = logging.getLogger(__name__)

## See if a node only contains literals
def isLit(node):
	if not node.inputPorts: return False
	for port in node.inputPorts:
		if not port.acceptsLiteral():
			return False
	return True

## Get all the inputs of a node (should only contain literals)
def getInputs(node):
	res = []
	for port in node.inputPorts:
		res.append(port.source.value)
	return res

##
# Create a DIS program to execute a 
# single operation.
##
def createOpStr(node):
	prog = dis.DIS(node.inputs)
	key = converter.convertNode(prog, node)
	prog.linkStart(key)
	prog.linkStop(key)
	return prog.generate()

##
# Create a DIS program to execute a
# single function.
##
def createCallStr(node):
	return graphConverter.convert(entryName = node.function)

## 
# Use DVM to execute a single operation 
# with it's literals as inputs.
##
def getValue(node):
	inputs = getInputs(node)

	str = None
	if isinstance(node, IGR.node.OperationNode):
		str = createOpStr(node)
	elif isinstance(node, IGR.node.CallNode):
		str = createCallStr(node)
	else: log.error("Found unknown literal node type %s", node)

	# Run the program
	val = dvm.run(dis = str, inputs = inputs)
	return val

##
# Add the result of executing
# a node to all it's outputs.
##
def transformNode(node, value): 
	for port in node.outputPorts:
		for port in port.targets:
			IGR.addLiteral(value, port.node, port.idx)

## Delete a node from the program.
def deleteNode(node):
	sg = node.subGraph
	sg.nodes.remove(node)

## See if a node can be removed, do so if possible.
def checkNode(node):
	if isLit(node):
		val = getValue(node)
		transformNode(node, val)
		deleteNode(node)
		log.info("Reducing node '%s' to literal '%s'", node, val)

## Remove all operations that have predefined inputs.
def removeLiterals():
	IGR.traverse(
		checkNode,
		lambda x: None,
		lambda x: None,
		False,
		lambda x: None,
		lambda x: None
		)
	converter.reset()