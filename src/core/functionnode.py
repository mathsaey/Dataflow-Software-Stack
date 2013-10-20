# FunctionNode.py
# Mathijs Saey
# dvm prototype

from abstractnode import AbstractNode
import port

# Represents a function, a function node is simply a collection of in and 
# output ports that gather the data needed to execute the function.
class FunctionNode(AbstractNode):

	def __init__(self, inputs, outputs):
		super(FunctionNode, self).__init__(inputs, outputs)
		self.fillList(self.inputs, port.OutputPort)
		self.fillList(self.outputs, port.OutputPort)

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.OutputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)
