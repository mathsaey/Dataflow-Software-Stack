# runtime.py
# Mathijs Saey
# dvm prototype

import copy
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

	def fetchLiterals(self):
		while not self.literalQueue.empty():
			lit = self.literalQueue.get()
			lit.activate()

	def run(self):
		self.fetchLiterals()
		while True:
			node = self.readyQueue.get()
			node.execute()

class FunctionPool(object):
	def __init__(self):
		super(FunctionPool, self).__init__()
		self.pool = {}

	def addFunction(self, key, node):
		self.pool.update({key : node})
		
	def getFunction(self, key):
		return copy.deepcopy(self.pool[key])

main = Scheduler()
pool = FunctionPool()

