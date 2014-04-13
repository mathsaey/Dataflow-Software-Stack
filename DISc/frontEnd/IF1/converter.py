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
##

import IGR
import IGR.node

def convertCall(node):
	subGraph = node.subGraph
	function = node.inputPorts[0].source.value
	callNode = IGR.node.CallNode(subGraph, function)
	subGraph.replaceNode(node, callNode)

	callNode.inputs -= 1
	callNode.inputPorts = callNode.inputPorts[1:]
	for port in callNode.inputPorts:
		port.idx -= 1

conversions = {
	'Call' : convertCall
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