# Edge.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Edge(DataConnector):
	"""Represents an edge between 2 nodes

	An edge knows the node that it originated from
	along with the port it leads to."""

	def __init__(self, source, destination):
		self.source = source
		self.destination = destination

	def acceptInput(self, input):
		print "Edge:", self, "accepted input:", input
		self.destination.acceptInput(input)