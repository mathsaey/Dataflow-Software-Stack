# AbstractNode.py
# Mathijs Saey
# dvm prototype

class AbstractNode(object):
	"""This class represents a node in any graph type."""
	
	def __init__(self,inputs):
		self.inputs = [None] * inputs
		self.outputs = []

	def addInput(self, idx, input):
		self.inputs[idx] = input

	def addOutput(self, output):
		self.outputs += [output]

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
			if el is None:
				return False
			elif el.ready():
				print 'top lel'
				return False
		return True
	
	def execute(self):
		raise NotImplementedError("Execute is an abstract method!")