# if1error.py
# Mathijs Saey
# dvm prototype

class IF1Error (Exception):
	""" This class represents an IF1 error. """

	def __init__(self, err = None):
		super(IF1Error, self).__init__()
		self.err = err

	def __str__(self):
		return "IF1 error: " + self.err

	def __eq__(self, other):
		return self.isErrValue() or self.err == other.err

	def isErrValue(self):
		return self.err is None