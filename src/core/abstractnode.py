# AbstractNode.py
# Mathijs Saey
# dvm prototype

import scheduler
import port
import edge

class AbstractNode(object):
	"""
	This class represents a node in any graph type.

	A Node contains an arbitrary amount of input nodes
	and an arbitrary amount of output edges.
	"""
	
	def __init__(self,inputs):
		""" Initialize a node with a predetermined amount of inputs """
		self.inputs = [None] * inputs
		self.outputs = []
		for i in xrange(0,inputs):
			self.inputs[i] = port.Port(self)

	def getInput(self, idx):
		""" Gets the input at idx """
		return self.inputs[idx]

	def addOutput(self, destination):
		""" Adds an output edge and returns it """
		e = edge.Edge(self, destination)
		self.outputs += [e]
		return e

	def getArguments(self):
		""" Gather the arguments from all the input ports """
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def sendOutput(self, output):
		""" Send a value to all the output edges """
		for el in self.outputs:
			el.acceptInput(output)

	def reset(self):
		""" Reset all input """
		for el in self.inputs:
			el.clear()

	def isInputReady(self):
		""" Check if all the ports have received inputs"""
		for el in self.inputs:
			if (el is None) or not el.ready():
				return False
		return True
	
	def receivedInput(self):
		""" Respond to a port receiving input"""
		if self.isInputReady():
			scheduler.main.addNode(self)

	def execute(self):
		""" 
		Consume all inputs, execute this node, send the 
		output and reset the node 
		"""
		raise NotImplementedError("Execute is an abstract method!")