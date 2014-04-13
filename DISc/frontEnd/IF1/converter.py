# convert.py
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
# \package frontEnd.IF1.convert
# \brief Node converter
# 
# This module converts some of the IF1 operations
# into different node types.
# Other operations are adjusted to remove semantic
# differences between IF1 and dis
##

import IGR
import IGR.node

import logging
log = logging.getLogger(__name__)

##
# See if a port utilizes a correct lower bound
# of an array.
##
def checkLowerBound(port, valid):
	if (not port.acceptsLiteral() or port.source.value != valid): 
		log.info("Converting invalid lower bound: %s", port)
		port.source.valid = 0

##
# Remove the first input port of a node.
# Update the indices of the other ports
# to reflect this.
##
def removeInputPort(node):
	node.inputs -= 1
	node.inputPorts = node.inputPorts[1:]
	for port in node.inputPorts:
		port.idx -= 1

##
# Convert ABuild.
#
# This operation remains relatively unchanged,
# we just remove the lower bound of the build operation.d
# We also emit a warning if the lower bound is not 0.
##
def convertABuild(node):
	node.operation = 'array'
	checkLowerBound(node.inputPorts[0], 0)
	removeInputPort(node)

	if node.inputs == 0:
		node.subGraph.removeNode(node)
		for port in node.outputPorts:
			for port in port.targets:
				IGR.addLiteral([], port.node, port.idx)

##
# Convert AFill.
# \see convertABuild
##
def convertAFill(node):
	node.operation = 'arrCreate'
	checkLowerBound(node.inputPorts[0], 0)
	removeInputPort(node)

##
# Convert AGather.
# The node that emerges from this
# has different semantics in DVM.
# In dvm, the second argument is an array
# that is already constructed.
#
# The merge instruction should be provided
# by the compiler when it's compiling compound nodes.
##
def convertAGather(node):
	node.operation = 'arrPrune'
	checkLowerBound(node.inputPorts[0], 0)
	removeInputPort(node)

##
# Convert AScatter.
#
# Once again, the actual split should
# be provided by the compiler.
##
def convertAScatter(node):
	pass

##
# Convert ALimL
#
# A DVM array always has a lower bound of 0.
# So we eliminate this node and add 0 as a literal.
##
def convertALimL(node):
	for port in node.outputPorts:
		for port in port.targets:
			IGR.addLiteral(0, port.node, port.idx)
	for port in node.inputPorts:
		port.source.removeTarget(port)
	node.subGraph.removeNode(node)	

##
# A lower bound of an array cannot be changed
# in DVM. Thus we remove this operation.
# We also return an error if the bound was 
# set to anything that is not 0
##
def convertASetL(node):
	arrPort = node.inputPorts[0]
	bndPort = node.inputPorts[1]
	checkLowerBound(bndPort, 0)

	targets = [target for port in node.outputPorts for target in port.targets]

	arrPort.source.removeTarget(arrPort)
	arrPort.source.addTargets(targets)
	node.subGraph.removeNode(node)	

## Convert a call operation to a call node.
def convertCall(node):
	subGraph = node.subGraph
	function = node.inputPorts[0].source.value
	callNode = IGR.node.CallNode(subGraph, function)
	subGraph.replaceNode(node, callNode)
	removeInputPort(callNode)

##
# Convert 'less chains'
#
# IF1 does not define a more or moreEq, 
# instead it adds a not after a < or =<
# This method looks for such a chain and replaces
# it if possible.
##
def convertLessChain(node, replacement):
	targets = node.outputPorts[0].targets
	notNode = node.outputPorts[0].targets[0].node

	if not (
		len(targets) == 1 and 
		isinstance(notNode, IGR.node.OperationNode) and 
		notNode.operation == 'not'
		): return

	node.operation = replacement
	node.subGraph.removeNode(notNode)
	node.outputPorts = notNode.outputPorts
	for port in node.outputPorts:
		port.node = node

## 
# Convert a less chain: 
# not smaller => greater or eq
##
def convertLess(node):
	convertLessChain(node, 'moreEq')

## 
# Convert a less chain: 
# not smaller or eq => greater
##
def convertLessEq(node):
	convertLessChain(node, 'more')

conversions = {
	'ABuild'   : convertABuild,
	'AFill'    : convertAFill,
	'AGather'  : convertAGather,
	'AScatter' : convertAScatter,
	'ALimL'    : convertALimL,
	'ASetL'    : convertASetL,
	'Call'     : convertCall,
	'less'     : convertLess,
	'lessEq'   : convertLessEq
}

def checkNode(node):
	if (
		isinstance(node, IGR.node.OperationNode) 
		and node.operation in conversions
		):
		conversions[node.operation](node)

def run():
	IGR.traverse(
		checkNode, 
		lambda x : None,
		lambda x : None,
		False,
		lambda x : None,
		lambda x : None
		)