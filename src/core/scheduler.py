# Scheduler.py
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
		while True:
			lit = self.literalQueue.get()
			lit.activate()

	def run(self):
		nodeThread = threading.Thread(target = self.fetchNodes, args = tuple())
		litThread = threading.Thread(target = self.fetchLiterals, args = tuple())
		nodeThread.start()
		litThread.start()

main = Scheduler()