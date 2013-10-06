# literal.py
# Mathijs Saey
# dvm prototype

class Literal(object):
	"""Represents an edge with no destination but a direct value"""
	
	def __init__(self, destination, value):
		self.destination = destination
		self.value = value

	def activate(self):
		self.destination.acceptInput(self.value)