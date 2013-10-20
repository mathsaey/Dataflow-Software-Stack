# Edge.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Edge(DataConnector):
	def __init__(self, source, destination):
		self.destination = destination
		self.source = source
		self.source.addEdge(self)

	def acceptInput(self, input):
		self.destination.acceptInput(input)