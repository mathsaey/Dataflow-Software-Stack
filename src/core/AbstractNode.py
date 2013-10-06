# AbstractNode.py
# Mathijs Saey
# dvm prototype

from port import Port

class AbstractNode(object):
	"""This class represents a node in any graph type.

		A Node contains an arbitrary amount of input nodes
		and an arbitrary amount of output edges.
	"""
	
	def __init__(self,inputs):
		self.inputs = [Port(self)] * inputs
		self.outputs = []

	def getInput(self, idx):
		return self.inputs[idx]

	def getOutput(self):
		return self.outputs

	def getArguments(self):
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def sendOutput(self, outputs):
		for el in self.outputs:
			el.acceptInput(output)

	def isInputReady(self):
		for el in self.inputs:
			if el is None:
				return False
			elif el.ready():
				return False
		return True
	
	def execute(self):
		raise NotImplementedError("Execute is an abstract method!")