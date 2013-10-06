# Port.py
# Mathijs Saey
# dvm prototype

class Port(object):
	"""This class represents an input to a node"""

	def __init__(self, node, idx):
		"""Creates the port and adds it to the node"""
		self.node = node
		node.addInput(idx,self)

	def value(self):
		return self.input

	def node(self):
		return self.node

	def acceptInput(self,input):
		print "Port:", self, "accepting input:", input
		self.input = input

	def ready(self):
		try:
			self.input
		except AttributeError:
			return False
		else:
			return True
