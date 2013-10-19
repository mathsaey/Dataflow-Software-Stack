# AbstractNode.py
# Mathijs Saey
# dvm prototype

import scheduler
import port

"""
@todo don't remove literals when resetting
"""

class AbstractNode(object):
	"""
	This class represents a node in any graph type.

	A Node contains an arbitrary amount of input nodes
	and an arbitrary amount of output edges.
	"""
	
	def __init__(self,inputs, outputs):
		""" Initialize a node with a predetermined amount of in -and outputs """
		self.inputs = [None] * inputs
		self.outputs = [None] * outputs
		for i in xrange(0,inputs):
			self.inputs[i] = port.InputPort(self)
		for i in xrange(0,outputs):
			self.outputs[i] = port.OutputPort(self)

	def getInput(self, idx):
		""" Gets the input at idx """
		return self.inputs[idx]

	def getOutput(self, idx):
		""" Gets the output at idx """
		return self.outputs[idx]

	def getArguments(self):
		""" Gather the arguments from all the input ports """
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def sendOutput(self, idx, output):
		""" Send a value to an output port """
		self.getOutput(idx).acceptInput(output)

	def sendOutputs(self, outputs):
		""" 
		Send a list of outputs, the amount of elements
		the list contains should match the amount of output ports
		"""
		for idx in xrange(0, len(self.outputs)):
			self.sendOutput(idx, outputs[idx])

	def reset(self):
		""" Reset all ports """
		for el in self.inputs:
			el.clear()
		for el in self.outputs:
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