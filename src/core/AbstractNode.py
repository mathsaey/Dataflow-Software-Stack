# AbstractNode.py
# Mathijs Saey
# dvm prototype

import port
import edge

class AbstractNode(object):
	"""This class represents a node in any graph type.

		A Node contains an arbitrary amount of input nodes
		and an arbitrary amount of output edges.
	"""
	
	def __init__(self,inputs):
		self.inputs = [None] * inputs
		self.outputs = []
		for i in xrange(0,inputs):
			self.inputs[i] = port.Port(self)

	def getInput(self, idx):
		return self.inputs[idx]

	def addOutput(self, destination):
		e = edge.Edge(self, destination)
		self.outputs += [e]
		return e

	def getArguments(self):
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def sendOutput(self, output):
		for el in self.outputs:
			el.acceptInput(output)

	def isInputReady(self):
		for el in self.inputs:
			if (el is None) or not el.ready():
				return False
		return True
	
	def receivedInput(self):
		if self.isInputReady():
			self.execute()

	def execute(self):
		raise NotImplementedError("Execute is an abstract method!")