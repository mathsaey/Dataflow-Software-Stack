# runtime.py
# Mathijs Saey
# dvm prototype

"""
The Scheduler module defines the scheduler, which is responsible
for executing nodes and adding literals to the runtime
"""

import Queue
import thread
import threading

class Scheduler(object):
	def __init__(self):
		super(Scheduler, self).__init__()
		self.literalQueue 	= Queue.Queue()
		self.readyQueue 	= Queue.Queue()

	def addLiteral(self, lit):
		self.literalQueue.put(lit)

	def addNode(self, node):
		self.readyQueue.put(node)

	def fetchNodes(self):
		while True:
			node = self.readyQueue.get()
			node.execute()

	def fetchLiterals(self):
		while not self.literalQueue.empty():
			lit = self.literalQueue.get()
			lit.activate()

	def run(self):
		self.fetchLiterals()
		self.fetchNodes()

class FunctionPool(object):
	def __init__(self):
		super(FunctionPool, self).__init__()
		self.pool = {}

	def addFunction(self, key, node):
		self.pool.update({key : node})
		
	def getFunction(self, key):
		return self.pool[key]

main = Scheduler()
pool = FunctionPool()

