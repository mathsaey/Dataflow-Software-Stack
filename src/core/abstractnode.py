# AbstractNode.py
# Mathijs Saey
# dvm prototype

# Represents any node type in a graph
class AbstractNode(object):

	# Creates the in and outputs lists with the desired lengthts
	# Subclasses should take care to fill the list with the desired port type
	def __init__(self,inputs, outputs):
		self.inputs = [None] * inputs
		self.outputs = [None] * outputs

	# Get the input at idx, expand the list if needed
	def getInput(self, idx):
		raise NotImplementedError("GetInput is an abstract method!")

	# Get the output at idx, expand the list if needed
	def getOutput(self, idx):
		raise NotImplementedError("GetOutput is an abstract method!")

	# Send a value to an output port
	def sendOutput(self, idx, output):
		self.getOutput(idx).acceptInput(output)

	# Send a list of outputs, the amount of elements
	# the list contains should match the amount of output ports
	def sendOutputs(self, outputs):
		for idx in xrange(0, len(self.outputs)):
			self.sendOutput(idx, outputs[idx])

	# Reset all ports
	def reset(self):
		for el in self.inputs:
			el.clear()
		for el in self.outputs:
			el.clear()

	# Fill a list with a given port type
	def fillList(self, lst, constructor):
		for idx in xrange(0, len(lst)):
			lst[idx] = constructor(self)

	# Fetches the element at idx
	# If the idx is not present, the list is expanded.
	# This allows us to define nodes that accept a non-constant amount of inputs
	def getFromList(self, lst, constructor, idx):
		try:
			res = lst[idx]
		except IndexError:
			lst += [constructor(self)]
			res = lst[idx]
		finally:
			return res
	