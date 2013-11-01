# runtime.py
# Mathijs Saey
# dvm prototype

# The MIT License (MIT)
#
# Copyright (c) 2013 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 		
# of this software and associated documentation files (the "Software"), to deal		      
# in the Software without restriction, including without limitation the rights		
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell		
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module controls in which order that various nodes and literals are executed
"""

import copy
import Queue

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

