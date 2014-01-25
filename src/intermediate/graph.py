# graph.py
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
# \file graph.py
# \namespace intermediate.graph
# \brief Complete program
# 
# This defines the complete program graph. All of the subgraphs
# as well as their names can be found here.
#
# This file also defines a few top level functions that 
# facilitate adding nodes, ports and literals to the IGR.
##

import subgraphs
import literals
import nodes

## All of the functions in the program 
__SUBGRAPHS__ = []

## The function names, combined with the subgraph they map to.
__FUNCTION_NAMES__ = {}


def _addSubGraph(subGraph):
	__SUBGRAPHS__.append(subGraph)

def _bindName(name, graph):
	__FUNCTION_NAMES__.update({name : graph})

##
# Create a new subgraph
#
# \param inputs
#		The amount of inputs the subgraph accepts
# \param outputs
# 		The amount of data the subgraph returns
# \return
# 		The entry exit pair belonging to the subgraph
#
def createSubGraph(name , inputs, outputs):
	graph = subgraphs.SubGraph(None, None, name)
	entry = nodes.SubGraphEntryNode(graph, inputs)
	exit  = nodes.SubGraphExitNodes(graph, outputs)
	graph.entry = entry
	graph.exit = exit
	_addSubGraph(graph)
	_bindName(name, graph)
	return (entry, exit)

##
# Connect 2 ports with an implicit edge.
#
# \param srcNode
#		The node that provides data
# \param srcPort
#		The idx of the output port on src
# \param dstNode
#		The node that accepts the data
# \param dstPort
#		The idx of the port on dst that accepts the data.
##
def connect(srcNode, srcPort, dstNode, dstPort):
	srcP = srcNode.getOutputPort(srcPort)
	dstP = dstNode.getInputPort(dstNode)
	srcP.addTarget(dstP)
	dstP.attach(srcP)

##
# Add a literal to a port.
#
# \param value
#		The value of the literal
# \param dstNode
#		The node that the literal targets
# \param dstPort
#		The idx of the port on this node
##
def addLiteral(value, dstNode, dstPort):
	dest = dstNode.getInputPort(dstPort)
	lit = literals.Literal(value, dest)
	dest.attach(lit)

##
# Create an operation node
#
# \param subGraph
#		The subGraph that this node is part of
#
# \param operation
#		The operation that this node performs
##
def createOperationNode(subGraph, operation):
	return nodes.OperationNode(subGraph, operation)

##
# Create a Compound nodes
#
# \param subGraph
#		The subgraph this node belongs too
# \param subGraphss
#		The subgraphs that are part of this compound node
##
def createCompoundNode(subGraph, subGraphs):
	return nodes.CompoundNode(subGraph, subGraphs)

##
# Create a call node.
#
# \param subGraph
# 		the subgraph this node belongs to
# \param inputs
#		the amount of inputs this 
##
def createCallNode(subGraph):
	return nodes.CallNode(subGraph)
