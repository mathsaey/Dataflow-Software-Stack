# OperationNode.py
# Mathijs Saey
# dvm prototype

from executablenode import ExecutableNode
import port

# Represents a single operation
class OperationNode(ExecutableNode):
	def __init__(self, inputs, outputs, operation):
		super(OperationNode, self).__init__(inputs, outputs)
		self.fillList(self.outputs, port.OutputPort)
		self.fillList(self.inputs, port.InputPort)
		self.operation = operation

	def __str__(self):
		id = super(OperationNode, self).__str__()
		return "OperationNode:\t(" + id + ")"

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.InputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

	def receivedInput(self):
		if self.isInputReady():
			self.addToScheduler()

	# Get all the input values
	def gatherInput(self):
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def execute(self):
		super(OperationNode, self).execute()
		lst = self.gatherInput()
		res = self.operation(*lst)
		self.sendOutputs([res])
		self.reset()

