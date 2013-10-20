# Edge.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Edge(DataConnector):
	"""
	Represents an edge between 2 nodes

	An edge knows the port that it originated from
	along with the port it leads to.
	"""

	def __init__(self, source, destination):
		self.destination = destination
		self.source = source
		self.source.addEdge(self)

	def acceptInput(self, input):
		self.destination.acceptInput(input)