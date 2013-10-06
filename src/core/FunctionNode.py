# FunctionNode.py
# Mathijs Saey
# dvm prototype

import AbstractNode

class FunctionNode(AbstractNode):
	"""An operation node represents a function that contains it's own graph.

	   When building the funciton node, care should be taken to wire the correct
	   input to the right edges.
	"""