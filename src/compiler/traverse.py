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
# \package compiler.traverse
# \brief IGR Traversals
# 
# This module defines the functions that allow us to
# traverse the IGR graph.
##

import igr

##
# Traverse all the nodes in the program.
#
# \param nodeProc
#		The function that is called when we encounter a node.
#		node is passed as an argument to this function.
# \param subGraphStart
#		The function that is called when we enter a new subgraph.
#		The subgraph is passed as an argument.
# \param subGraphStop
#		The function that is called when we exit a subgraph.
#		The subgraph is passed as an argument.
# \param skipCompound
#		Should be true is you want to treat compounds as normal nodes.
#		If this value is false, the subgraphs of any compound node will
#		be traversed.
# \param compoundStart
#		The function that is called when we start parsing a compound node.
#		The node is passed as an argument to this function.
#		Remember that we have already called nodeProc on this node!
# \param comoundEnd
#		The function that is called when we exit a compound node.
#		The node in question is passed to the function.
# \param subGraphs
#		The subgraphs to traverse. Parses the entire program by default.
##
def traverseAll(
 	nodeProc, 
	subGraphStart,
	subGraphStop, 
	skipCompound,
	compoundStart,
	compoundStop,
	subGraphs = igr.getSubGraphs()
	):

	def traverseSubGraph(subGraph, nodeProc):
		subGraphStart(subGraph)
		for node in subGraph.nodes:
			nodeProc(node)
			checkCompound(node)
		subGraphStop(subGraph)

	def checkCompound(node):
		if (not skipCompound) and (node.isCompound()):
			compoundStart(node)
			traverseAll(
				nodeProc,
				subGraphStart,
				subGraphStop,
				skipCompound,
				compoundStart,
				compoundStop,
				node.subGraphs
				)
			compoundStop(node)

	for subGraph in subGraphs:
		traverseSubGraph(subGraph, nodeProc)
