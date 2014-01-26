# traverse.py
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
# \file compiler/traverse.py
# \namespace compiler.traverse
# \brief IGR Traversals
# 
# This module defines different functions that allow
# us to traverse the IGR in various ways.
##

import igr
import visitor

# ------------------- #
# SubGraph Traversals #
# ------------------- #
## \name SubGraph Traversals
## Traversals that iterate over a subgraph
## \{

##
# Traverses every node in a subgraph, in the order
# that the parser encountered them.
#
# \param nodeProc
#		The function to call when we encounter a node.
##
def traverseNodes(subGraph, nodeProc):
	for node in subGraph.nodes:
		nodeProc(node)

##
# Traverse the nodes in the subgraph, starting from
# the entry point and heading down following the edges
# in a depth-first manner.
#
# Depending on the way the subgraph is wired, this 
# traversal may not encounter all the nodes. Only the nodes
# that are (indirectly) connected to the entryNode are encountered.
#
# \param nodeProc
#		The function to call when we encounter a node.
##
def traverseTopToBottom(subGraph, nodeProc):
	v = visitor.ForwardVisitor(nodeProc)
	v.start(subGraph)

##
# Traverse the nodes in the subgraph, starting from the
# exit point and heading up following the incoming edges of 
# every node.
#
# Only the nodes that are (indirectly) wired to the exit node
# are encountered.
#
# \param nodeProc
#		The function to call when we encounter a node.
# \param literalProc
#		The function to call when we encounter a literal.
##
def traverseBottomToTop(subGraph, nodeProc, literalProc):
	v = visitor.BackwardVisitor(nodeProc, literalProc)
	v.start(subGraph)

## \}

# --------------------- #
# Full Graph Traversals #
# --------------------- #
## \name Full Graph Traversals
## Traversals that iterate over the complete program.
## \{

##
# Traverse all the subgraphs in the program.
#
# All of the other program traversals are defined in terms of this.
#
# \param subGraphStart
#		The function to call when we encounter a subgraph.
# \param subGraphStop
#		The function to call when we exit a subgraph.
# \param traversal
#		The function that performs the subgraph traversal.
# \param traversalArgs
#		The arguments that the traversal needs (without the subgraph)
##
def traverseAll(subGraphStart, subGraphStop, traversal, traversalArgs):
	for subGraph in igr.getSubGraphs():
		subGraphStart(subGraph)
		args = [subGraph] + traversalArgs
		traversal(*args)
		subGraphStop(subGraph)

##
# Traverse every node in the graph.
##
def traverseAllNodes(subGraphStart, subGraphStop, nodeProc):
	traverseAll(subGraphStart, subGraphStop, traverseNodes, [nodeProc])

##
# Traverse every subgraph with traverseTopToBottom()
#
# \param subGraphStart
#		The function to call when we encounter a subgraph.
# \param subGraphStop
#		The function to call when we exit a subgraph.
# \param nodeProc
#		The function to call when we encounter a node.
##
def traverseAllTopToBottom(subGraphStart, subGraphStop, nodeProc):
	traverseAll(subGraphStart, subGraphStop, traverseTopToBottom, [nodeProc])
##
# Traverse every subgraph with traverseBottomToTop()
#
# \param subGraphStart
#		The function to call when we encounter a subgraph.
# \param subGraphStop
#		The function to call when we exit a subgraph.
# \param nodeProc
#		The function to call when we encounter a node.
# \param literalProc
#		The function to call when we encounter a literal.
##
def traverseAllBottomToTop(subGraphStart, subGraphStop, nodeProc, literalProc):
	traverseAll(subGraphStart, subGraphStop, traverseBottomToTop, [nodeProc, literalProc])

## \}
