# nodes.py
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
# \package IGR.node
# \brief Node definitions
# 
# IGR node types. 
##

import port

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
	# \param inputs
	#		The amount of inputs this node will accept
	#		This argument is optional, the input amount
	# 		will be updated depending on the amount of 
	#		incoming edges.
	# \param outputs
	#		The amount of outputs this node will return.
	#		The same rules that apply to inputs apply here.
	##
	def __init__(self, subGraph, inputs = 0, outputs = 0):
		super(Node, self).__init__()
		self.subGraph    = subGraph
		self.key         = getKey()
		self.inputs      = inputs
		self.outputs     = outputs
		self.inputPorts  = [port.InputPort(self, i) for i in xrange(0,inputs)]
		self.outputPorts = [port.OutputPort(self, i) for i in xrange(0,outputs)]

	##
	# Create a printable version of the node
	##
	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	##
	# Gets an input port. Create it if it doesn't exist yet.
	# This allows us to determine the amount of inputs
	# a certain node will have, even if this is not explicit in IF1
	#
	# \param idx
	# 		The idx of the port you need
	# \return
	#		The port at idx
	##
	def getInputPort(self, idx):
		try:
			res = self.inputPorts[idx]
			return res
		except IndexError:
			self.inputs += 1
			self.inputPorts += [port.InputPort(self, idx)]
			return self.getInputPort(idx)

	##
	# Gets an output port. Create it if it doesn't exist yet.
	# This allows us to determine the amount of outputs
	# a certain node will have, even if this is not explicit in IF1
	#
	# \param idx
	# 		The idx of the port you need
	# \return
	#		The port at idx
	##
	def getOutputPort(self, idx):
		try:
			res = self.outputPorts[idx]
			return res
		except IndexError:
			self.outputs += 1
			self.outputPorts += [port.OutputPort(self, idx)]
			return self.getOutputPort(idx)


	## See if this node can be followed to other nodes.
	def hasNext(self): return True

	## See if this node can be follow to other nodes.
	def hasPrevious(self): return True

	## Check if this node is a compound node
	def isCompound(self): return False

	## Check if this node is a call node
	def isCall(self): return False


# --------------------------- #
# Graph entry and exit points #
# --------------------------- #

##
# Entry point of a subgraph.
# 
# Defines the topmost point of a subgraph.
# Nodes in the subgraph use this node to get their inputs.
#
# This corresponds to the values of the parameters for a function
# invocation.
##
class SubGraphEntryNode(Node): 

	def __init__(self, subGraph, outputs):
		super(SubGraphEntryNode, self).__init__(subGraph, 0, outputs)
		self.inputPorts = []

	def getInputPort(self, idx): return None
	def hasPrevious(self): return False

##
# Exit point of a subgraph.
# 
# Defines the leaves of a subgraph.
# Nodes in the subgraph use this node to dump their outputs.s
#
# This corresponds to the return value of a function.
##
class SubGraphExitNode(Node): 

	def __init__(self, subGraph, inputs):
		super(SubGraphExitNode, self).__init__(subGraph, inputs, 0)
		self.outputPorts = []

	def hasNext(self): return False
	def getOutputPort(self, idx): return None

# -------------- #
# Standard Nodes #
# -------------- #

##
# Operation node
#
# This class defines a standard dataflow operation.
# It contains the standard in and output ports along with
# the function that it represents.
##
class OperationNode(Node):
	def __init__(self, subGraph, operation):
		super(OperationNode, self).__init__(subGraph)
		self.operation = operation

	def __str__(self):
		key = str(self.key)
		opname = self.operation
		return "OpN '" + key + "' " + opname 

##
# Call node
#
# Represents an operation that calls a function (a subgraph)
# The output ports of the callnode are bound to the return values of the function.
##
class CallNode(Node):
	def __init__(self, subGraph):
		super(CallNode, self).__init__(subGraph)
		self.function = None

	def __str__(self):
		func = str(self.function)
		return "CallN '%d' %s" % (self.key, func)

	##
	# Binds the call node to a certain value.
	# Can be a graph, a graph identifier or a name.
	# The exact value depends on the stage.
	##
	def bindFunction(self, func):
		self.function = func

	def isCall(self): return True
	
# -------------- #
# Compound Nodes #
# -------------- #

##
# Compound node
#
# Represents a node that contains subgraphs.
# Examples of such nodes include if-then-else, for loops, ...
##
class CompoundNode(Node):
	def __init__(self, subGraph, subGraphs):
		super(CompoundNode, self).__init__(subGraph)
		self.subGraphs = subGraphs

	def isCompound(self): return True


## \todo Add in and outputs to nodes where this is known in advance (e.g. select)

class ForallCNode(CompoundNode): pass
class SelectCNode(CompoundNode): pass
class TagCaseCNode(CompoundNode): pass
class LoopACNode(CompoundNode): pass
class LoopBCNode(CompoundNode): pass
class IfThenElseCNode(CompoundNode): pass
class IterateCNode(CompoundNode): pass
class WhileLoopCNode(CompoundNode): pass
class RepeatLoopCNode(CompoundNode): pass
class SeqForallCNode(CompoundNode): pass
class UReduceCNode(CompoundNode): pass