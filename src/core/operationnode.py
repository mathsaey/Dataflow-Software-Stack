# OperationNode.py
# Mathijs Saey
# dvm prototype

from abstractnode import AbstractNode

class OperationNode(AbstractNode):
	"""An operation node represents a single operation in a dataflow graph"""

	def __init__(self, inputs, outputs, operation):
		super(OperationNode, self).__init__(inputs, outputs)
		self.operation = operation

	def execute(self):
		print "Node:", self, "executing..."
		lst = self.getArguments()
		res = self.operation(*lst)
		self.sendOutputs([res])
		self.reset()