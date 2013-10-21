# Port.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Port(DataConnector):
	""" Represents a port, a port contains the in- or output data of a node"""
	def __init__(self, node):
		self.node = node
		self.input = None
		self.fromLiteral = False

	def __str__(self):
		idx = None
		typ = None

		try:
			idx = self.node.inputs.index(self)
			typ = "Input "
		except ValueError:
			idx = self.node.outputs.index(self)
			typ = "Output"

		return typ + " port " + str(idx) + " of node " + str(self.node)

	def value(self):
		return self.input

	def node(self):
		return self.node

	def acceptInput(self,input, fromLiteral):
		print "Port:", self, "accepted input:", input
		self.fromLiteral = fromLiteral
		self.input = input

	def ready(self):
		return self.input is not None

	def clear(self):
		if not self.fromLiteral:
			self.input = None

class InputPort(Port):
	""" Represents a port that keeps it's input until the node is ready"""
	def acceptInput(self,input, fromLiteral = False):
		super(InputPort, self).acceptInput(input, fromLiteral)
		self.node.receivedInput()

class OutputPort(Port):	
	""" Represents a port that just forwards it's input right away """
	def __init__(self, node):
		super(OutputPort, self).__init__(node)
		self.edges = []

	def addEdge(self, edge):
		self.edges += [edge]
		if self.ready():
			edge.acceptInput(self.input)

	def acceptInput(self,input, fromLiteral = False):
		super(OutputPort, self).acceptInput(input, fromLiteral)
		for el in self.edges:
			el.acceptInput(input)