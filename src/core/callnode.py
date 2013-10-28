# callnode.py
# Mathijs Saey
# dvm prototype

from executablenode import ExecutableNode
import runtime
import edge
import port

# Represents a node that will look up a function at runtime and call it
# The name of the function to call will be added on the first port
class CallNode(ExecutableNode):

	def __init__(self, inputs, outputs):
		super(CallNode, self).__init__(inputs, outputs)
		self.fillList(self.inputs, port.OutputPort)
		self.fillList(self.outputs, port.OutputPort)
		self.inputs[0] = port.InputPort(self, 0)

	def __str__(self):
		id = super(CallNode, self).__str__()
		return "CallNode: (" + id + ")"

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.OutputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

	def receivedInput(self, idx):
		if idx is 0:
			self.addToScheduler()

	# Find the function to execute and "wire" it.
	def execute(self):
		super(CallNode, self).execute()
		key = self.inputs[0].value()
		func = runtime.pool.getFunction(key)
		for idx in xrange(0,len(func.outputs)):
			src = func.getOutput(idx)
			dst = self.getOutput(idx)
			edge.Edge(src, dst)
		for idx in xrange(0,len(func.inputs)):
			src = self.getInput(idx + 1)
			dst = func.getInput(idx)
			edge.Edge(src, dst)

