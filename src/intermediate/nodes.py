# nodes.py
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
# \file nodes.py
# \namespace intermediate.nodes
# \brief Node definitions
# 
# IGR node types. 
##

import ports

# ------------------ #
# Unique Identifiers #
# ------------------ #

__KEY__ = 0

##
# Generate unique id.
#
# Generate a key that serves as a unique
# id for a node.
# Mainly useful for debugging purposes.
##
def getKey():
	global __KEY__
	i = __KEY__
	__KEY__ += 1
	return i

# ----- #
# Nodes #
# ----- #

##
# Standard node.
#
## 
class Node(object):

	##
	# Create a new node.
	#
	# \param subGraph
	#		The subgraph this node belongs to.
	##
	def __init__(self, subGraph):
		super(Node, self).__init__()
		self.subGraph = subGraph
		self.key = getKey()

	##
	# Create a printable version of the node
	##
	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	## 
	# Fetch an element from a list and expand the list if it
	# is not long enough. 
	# 
	# This allows us to find out the exact amount of inputs and
	# outputs that a certain node produces even if we cannot know
	# this in advance (for instance, call nodes).
	#
	# \param lst
	#		The list from which we want to grab an element
	# \param var
	#		The var to update if we had to expand the list
	# \param constructor
	#		The constructor to use when expanding the list.
	# \param idx
	#		The idx of the element we want
	##
	def getFromList(self, lst, var, constructor, idx):
		try:
			res = lst[idx]
			return res
		except IndexError:
			var += 1
			lst += [constructor(self, idx)]
			return self.getFromList(lst, constructor, idx)

# --------------------------- #
# Graph entry and exit points #
# --------------------------- #

##
# Parent of SubGraphEntryNode and SubGraphExitNode.
# Mainly introduced to remove common code.
##
class AbstractSubGraphNode(Node):

	##
	# Initialize a subgraphnode. 
	#
	# \param subGraph
	#		The graph this node belongs to
	# \param slots
	#		The amount of ports this node has.
	# \param constructor
	# 		The constructor for the port type of the slots
	##
	def __init__(self, subGraph, slots, constructor):
		super(SubGraphEntryNode, self).__init__(self, subGraph)
		self.slots = slots
		self.ports = [constructor(self, i) for i in xrange(0,slots)]

	##
	# Get a port, extend the list if it's out of bounds.
	# 
	# \param idx
	#		The idx of the port
	##
	def getPort(self, idx): pass

##
# Entry point of a subgraph.
# 
# Defines the topmost point of a subgraph.
# Nodes in the subgraph use this node to get their inputs.
#
# This corresponds to the values of the parameters for a function
# invocation.
##
class SubGraphEntryNode(AbstractSubGraphNode): 

	def __init__(self, subGraph, slots = 0):
		super(SubGraphEntryNode, self).__init__(self, subGraph, ports.OutputPort)

	def getPort(self, idx):
		self.getFromList(self.slotList, self.slots, ports.OutputPort, idx)

##
# Exit point of a subgraph.
# 
# Defines the leaves of a subgraph.
# Nodes in the subgraph use this node to dump their outputs.s
#
# This corresponds to the return value of a function.
##
class SubGraphExitNode(AbstractSubGraphNode): 

	def __init__(self, subGraph, slots = 0):
		super(SubGraphExitNode, self).__init__(self, subGraph, ports.InputPort)

	def getPort(self, idx):
		self.getFromList(self.slotList, self.slots, ports.InputPort, idx)


# -------------- #
# Standard Nodes #
# -------------- #

##
# Node with in and output ports.
#
# This class represents the more common node type of nodes 
# that have both in and output ports.
##
class StandardNode(Node):

	##
	# Initialize a node.
	#
	# \param subGraph
	#		The subGraph this node belongs to.
	# \param inputs
	#		The amount of inputs this node accepts.
	# \param outputs 
	#		The amount of outputs this node produces.
	##
	def __init__(self, subGraph):
		super(StandardNode, self).__init__(subGraph)
		self.inputs      = 0
		self.outputs     = 0
		self.inputPorts  = []
		self.OutputPorts = []

	##
	# Gets an input port
	#
	# \param idx
	# 		The idx of the port you need
	# \return
	#		The port at idx
	##
	def getInputPort(self, idx):
		self.getFromList(self.inputPorts, self.inputs, ports.InputPort, idx)

	##
	# Gets an output port
	#
	# \param idx
	# 		The idx of the port you need
	# \return
	#		The port at idx
	##
	def getOutputPort(self, idx):
		self.getFromList(self.OutputPorts, self.outputs, ports.OutputPort, idx)


##
# Operation node
#
# This class defines a standard dataflow operation.
# It contains the standard in and output ports along with
# the function that it represents.
##
class OperationNode(StandardNode):

	def __init__(self, subGraph, operation):
		super(OperationNode, self).__init__(subGraph)
		self.operation = operation

##
# Call node
#
# Represents an operation that calls a function (a subgraph)
# The output ports of the callnode are bound to the return values of the function.
##
class CallNode(StandardNode):

	def __init__(self, subGraph):
		super(CallNode, self).__init__(subGraph)
		self.function = None

	##
	# Binds the call node to a certain value.
	# Can be a graph, a graph identifier or a name.
	# The exact value depends on the stage.
	##
	def bindFunction(self, func):
		self.function = func

##
# Compound node
#
# Represents a node that contains subgraphs.
# Examples of such nodes include if-then-else, for loops, ...
##
class CompoundNode(StandardNode):

	def __init__(self, subGraph, subGraphs):
		super(CompoundNode, self).__init__(subGraph)
		self.subGraphs = subGraphs