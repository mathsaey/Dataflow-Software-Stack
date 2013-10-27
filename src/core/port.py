# Port.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Port(DataConnector):
	""" Represents a port, a port contains the in- or output data of a node"""
	def __init__(self, node, idx, typ = "Unknown"):
		self.idx = idx
		self.typ = typ
		self.node = node
		self.input = None
		self.fromLiteral = False

	def __str__(self):
		return self.typ + "port " + str(self.idx) + " of node " + str(self.node)

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
	def __init__(self, node, idx = "?"):
		super(InputPort, self).__init__(node, idx, "Input")

	def acceptInput(self,input, fromLiteral = False):
		super(InputPort, self).acceptInput(input, fromLiteral)
		self.node.receivedInput()

class OutputPort(Port):	
	""" Represents a port that just forwards it's input right away """
	def __init__(self, node, idx = "?"):
		super(OutputPort, self).__init__(node, idx, "Output")
		self.edges = []

	def addEdge(self, edge):
		self.edges += [edge]
		if self.ready():
			edge.acceptInput(self.input)

	def acceptInput(self,input, fromLiteral = False):
		super(OutputPort, self).acceptInput(input, fromLiteral)
		for el in self.edges:
			el.acceptInput(input)