# CompoundNode.py
# Mathijs Saey
# dvm prototype

from executablenode import ExecutableNode

class CompoundNode(ExecutableNode):
	"""A Compound node represents a more complex node that contains subgraphs"""

	def __init__(self, inputs, outputs, subgraphs):
		super(CompoundNode, self).__init__(inputs)
		self.subgraphs = subgraphs


class IfThenElseNode(CompoundNode):
	