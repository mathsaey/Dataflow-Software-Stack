# CompoundNode.py
# Mathijs Saey
# dvm prototype

from abstractnode import AbstractNode

class CompoundNode(AbstractNode):
	"""A Compound node represents a more complex node that contains subgraphs"""

	def __init__(self, inputs):
		super(CompoundNode, self).__init__(inputs)
