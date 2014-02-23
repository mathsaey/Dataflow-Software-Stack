# environment.py
# Mathijs Saey
# IDIS

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
# \package if1parser.environment
# \brief Node lookup and scoping rules.
# 
# This module contains the "state" of the parser.
# It keeps track of the discovered nodes and graphs
# and the scopes they are in. 
##

import tools

# ----- #
# Frame #
# ----- #

##
# Single part of the scope stack.
# 
# A scope contains all of the definitions
# of the current scope.
#
##
class Scope(object):

	##
	# Create a scope belonging to a subgraph.s
	# By convention, the subgraph can always be 
	# found at label 0.
	##
	def __init__(self, subGraph = None):
		super(Scope, self).__init__()
		self.nodes = [subGraph]

	##
	# Add a node to the scope.
	#
	# The label of the node should match
	# the current length of the node list of this object.
	# This is the case since IF1 nodes start are sequentially
	# numbered starting from one.
	#
	# \param label
	# 		The IF1 label of the node.
	# \param node
	#		The IGR node to assign to the label
	##
	def addNode(self, label, node):
		if len(self.nodes) is label:
			self.nodes += [node]
		else:
			# This situation can occur in IF1 (might be a bug)
			# so fill the list with none until the length is ok.
			tools.warning("Non-sequential node label added!")
			padding = [None for i in xrange(0, label - len(self.nodes))]
			self.nodes += padding
			self.addNode(label, node)

	##
	# Get a node from the scope.
	#
	# \param label
	#		The label of the node to get
	##
	def getNode(self, label):
		return self.nodes[label]

	##
	# Get the subgraph of the scope.
	##
	def getSubGraph(self):
		return self.nodes[0]

##
# Single part of the scope stack.
#
# This scope is only to be used inside the global
# environment of a compound node. It is meant to store
# the various subgraphs of a compound node.
##
class CompoundScope(object):
	def __init__(self):
		super(CompoundScope, self).__init__()
		self.graphs = []

	##
	# Add a graph to the list of subgraphs
	##
	def addSubGraph(self, graph):
		self.graphs.append(graph)

# ------- #
# Scoping #
# ------- #

##
# A stack with the global scope at the bottom,
# and the current scope at the top.
##
__STACK__ = [Scope()]

##
# Create a new scope and push
# it on top of the stack.
##
def scope(subGraph):
	global __STACK__
	__STACK__ = [Scope(subGraph)] + __STACK__

##
# Create a new compound scope and push it
# on top of the stack.
##
def scopeCompound():
	global __STACK__
	__STACK__ = [CompoundScope()] + __STACK__

##
# Remove the current scope.
# Returns to the previous scope.
##
def popScope():
	global __STACK__
	if len(__STACK__) > 1:
		__STACK__ = __STACK__[1:]

##
# Get the node with label in the current scope.
#
# \param label
#		The label to look for.
##
def getNode(label):
	return __STACK__[0].getNode(label)

##
# Add node with label to the current scope.
#
# \param label
#		The IF1 label of the node.
# \param node
#		The node to add
##
def addNode(label, node): 
	__STACK__[0].addNode(label, node)

##
# Get the subgraph of the current scope.
##
def getSubGraph():
	return __STACK__[0].getSubGraph()

##
# Add a subgraph to the compound scope.
# This will cause errors if the current
# scope is not a compound scope.
##
def addSubGraph(graph):
	__STACK__[0].addSubGraph(graph)

##
# Get the subgraphs.
# This will cause errors if the current
# scope is not a compound scope.
##
def getSubGraphs():
	return __STACK__[0].graphs

# ----------------- #
# Compound Checking #
# ----------------- #

## 
# Keeps track of the level of depth
# w.r.t. a compound definition.
# 
# This allows us to handle nested compound
# nodes without issues.
##
__COMP_LEVEL__ = 0

## Are we currently in a compound node?
def isCompound():
	return __COMP_LEVEL__ is not 0

## Enter a compound node.
def enterComp():
	global __COMP_LEVEL__
	__COMP_LEVEL__ += 1

## Exit a compound node.
def exitComp():
	global __COMP_LEVEL__
	__COMP_LEVEL__ -= 1