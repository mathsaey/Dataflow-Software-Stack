# FunctionNode.py
# Mathijs Saey
# dvm prototype

from abstractnode import AbstractNode
import port

class FunctionNode(AbstractNode):
	"""An operation node represents a function that contains it's own graph.

	   When building the function node, care should be taken to wire the correct
	   input to the right edges.
	"""

	def __init__(self, inputs, outputs):
		super(FunctionNode, self).__init__(inputs, outputs)
		for i in xrange(0,self.inputs):
			self.inputs[i] = port.OutputPort(self)