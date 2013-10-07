# Port.py
# Mathijs Saey
# dvm prototype

from dataconnector import DataConnector

class Port(DataConnector):
	"""This class represents an input or output of a node"""

	def __init__(self, node):
		"""Creates the port and adds it to the node"""
		self.node = node
		self.input = None

	def value(self):
		return self.input

	def node(self):
		return self.node

	def acceptInput(self,input):
		print "Port:", self, "accepting input:", input
		self.input = input
		self.node.receivedInput()

	def ready(self):
		return self.input is not None
