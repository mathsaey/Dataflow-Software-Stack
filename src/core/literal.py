# literal.py
# Mathijs Saey
# dvm prototype

import runtime

class Literal(object):	
	def __init__(self, destination, value):
		self.destination = destination
		self.value = value
		runtime.main.addLiteral(self)

	def activate(self):
		self.destination.acceptInput(self.value, True)
