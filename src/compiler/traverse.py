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
# This module defines the traversal operations.
# These traversals allow us to iterate over the IGR graph.
##

import igr

##
# This abstract class allows us to implement various
# traversals in terms of a few basic methods.
#
# By default it contains a list of the nodes that it
# has already visited and a function to invoke any time
# it encounters a new node. This function should accept
# the node as argument.
##
class AbstractVisitor(object):

	##
	# Create a new traversal with the given
	# nodeProc.
	#
	# \param nodeProc
	#		The function to call when we encounter
	#		a new node. should accept a node as argument.
	##
	def __init__(self, nodeProc):
		super(AbstractVisitor, self).__init__()
		self.nodeProc = nodeProc
		self.found = []

	##
	# Reset the found list in case the 
	# object should be reused.
	##
	def reset(self):
		self.found = []

	##
	# Start traversal on a given subgraph
	## 
	def start(self, subGraph): pass

	##
	# Called for every node we visit.
	# Determines the order of the various calls.
	# (preorder, inorder, postorder).
	##
	def visitNode(self, node): pass

	##
	# Called by visitNode(). Determines
	# how the children are fetched and the
	# order to call them in.
	##
	def visitChildren(self, node): pass

##
# A visitor that executes the traversal in a
# depth-first, preorder way.
##
class DepthFirstVisitor(AbstractVisitor):
	def visitNode(self, node):
		if node not in self.found:
			self.nodeProc(node)
			self.found.append(node)
			self.visitChildren(node)

##
# Traverses in a depth first, preorder,
# top to bottom way.
##
class ForwardVisitor(DepthFirstVisitor):

	def start(self, subGraph):
		self.visitNode(subGraph.entry)

	def visitChildren(self, node):
		for ports in node.outputPorts:
			for port in ports.targets:
				self.visitNode(port.node)

##
# Travers from the bottom up,
# such as from the return of a 
# function call.
##
class BackwardVisitor(DepthFirstVisitor):
	def __init__(self, nodeProc, literalProc):
		super(BackwardVisitor, self).__init__(nodeProc)
		self.literalProc = literalProc

	def start(self, subGraph):
		self.visitNode(subGraph.exit)

	def visitChildren(self, node):
		if node.hasPrevious(): 
			for port in node.inputPorts:
				if port.source:
					if port.source.isPort():
						self.visitNode(port.source.node)
					else: 
						self.literalProc(port.source)

##
# Traverse all of the subGraphs in the system.
#
# \param subGraphEncounter
#		Function to call when we see a new subgraph
# \param visitor
#		The visitor class to traverse the various subgraphs.
## 
def traverseAll(subGraphEncounter, visitor):
	for sub in igr.getSubGraphs():
		subGraphEncounter(sub)
		visitor.start(sub)
