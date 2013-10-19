# Port.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Port(DataConnector):
	def __init__(self, node):
		self.node = node
		self.input = None

	def value(self):
		return self.input

	def node(self):
		return self.node

	def acceptInput(self,input):
		print "Port:", self, "accepted input:", input
		self.input = input

	def ready(self):
		return self.input is not None

	def clear(self):
		self.input = None

class InputPort(Port):
	def __init__(self, node):
		super(InputPort, self).__init__(node)
		self.fromLiteral = False

	def acceptInput(self,input, fromLiteral = False):
		super(InputPort, self).acceptInput(input)
		self.fromLiteral = fromLiteral
		self.node.receivedInput()

	def clear(self):
		if not self.fromLiteral:
			self.input = None

class OutputPort(Port):	
	def __init__(self, node):
		super(OutputPort, self).__init__(node)
		self.edges = []

	def addEdge(self, edge):
		self.edges += [edge]

	def acceptInput(self,input):
		super(OutputPort, self).acceptInput(input)
		for el in self.edges:
			el.acceptInput(input)