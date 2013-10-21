# executablenode.py
# Mathijs Saey
# dvm prototype

from abstractnode import AbstractNode
import runtime

class ExecutableNode(AbstractNode):
	def isInputReady(self):
		""" Check if all the ports have received inputs"""
		for el in self.inputs:
			if (el is None) or not el.ready():
				return False
		return True

	# Signal the scheduler that the node is ready
	def addToScheduler(self):
		runtime.main.addNode(self)

	# Respond to a port receiving input
	def receivedInput(self):
		raise NotImplementedError("ReceivedInput is an abstract method!")
	
	# Called by the scheduler, what happens depends on the node type
	def execute(self):
		print "Node:", self, "executing..."

