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

## Get all the literal inputs of a node.
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
# single function call.
##
def createCallStr(node):
	return graphConverter.convert(entryName = node.function)

##
# Add the result of executing
# a node to all it's outputs.
##
def transformNode(node, value): 
	for port in node.outputPorts:
		for port in port.targets:
			IGR.addLiteral(value, port.node, port.idx)	

##
# Calculate the value of a literal
# and propagate it to the next nodes.
##
def propagateLit(node):
	str = None
	if isinstance(node, IGR.node.OperationNode):
		str = createOpStr(node)
	elif isinstance(node, IGR.node.CallNode):
		str = createCallStr(node)
	elif isinstance(node, IGR.node.SubGraphExitNode):
		val = getInputs(node)[0]
		node.subGraph.reduce(val)
		node.subGraph.removeNode(node)
		log.info("Reduced trivial graph: %s", node.subGraph)
		return
	else:
		log.error("Literals added to unsupported node: %s", node)
		return	

	val = dvm.run(dis = str, inputs = getInputs(node))	
	node.subGraph.removeNode(node)
	transformNode(node, val)
	log.info("Reducing node '%s' to literal '%s'", node, val)

##
# See if a call can be reduced to a 
# constant. If possible, propagate.
##
def checkCall(node):
	graph = IGR.getSubGraph(node.function)
	if graph.isTrivial():
		transformNode(node, graph.value)
		node.subGraph.removeNode(node)
		log.info("Replacing call '%s' with constant '%s'", node, graph.value)

## See if a node can be removed, do so if possible.
def checkNode(node):
	if isLit(node):
		propagateLit(node)
	elif isinstance(node, IGR.node.CallNode):
		checkCall(node)	

##
# See if we can remove a graph from the program.
# This assumes that it does not have to deal with 
# compound node subgraphs!
##
def checkGraph(subGraph):
	if subGraph.isTrivial():
		if subGraph.isFunc:
			IGR.removeSubGraph(subGraph)
			log.info("Removing trivial function graph %s", subGraph)
		else:
			# Remove the subgraph by a constant, followed by the exit node.
			const = IGR.createConstantNode(subGraph, subGraph.value)
			subGraph.entry = const
			subGraph.nodes = [const , subGraph.exit]
			IGR.connect(const, 0, subGraph.exit, 0)
			log.info("Replacing trivial graph %s by constant: %s", subGraph, const)

## Remove all operations that have predefined inputs.
def removeLiterals():
	IGR.traverse(
		checkNode,
		lambda x: None,
		lambda x: checkNode(x.exit),
		False,
		lambda x: None,
		lambda x: None
		)
	IGR.traverse(
		lambda x : None,
		checkGraph,
		lambda x : None,
		False,
		lambda x : None,
		lambda x : None
		)

