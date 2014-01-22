# environment.py
# Mathijs Saey
# dvm prototype

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
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
if1 scope definitions.

This module keeps track of the instructions that we added to the api and the
nodes that they map to.

The following functions are available for use by other modules:

scope():
	Add a new scope to the stack

popScope():
	Pop the current scope

getInst(node):
	Get a node in the current scope
addNode(node, inst):
	Get the instance key that matches a given node
getSubGraphExit():
	Get the instruction key of the subgraph exit
getSubGraphEntry(): 
	Get the instruction key of the subgraph entry
addSubGraph(enter, exit):
	Set the subgraph of the current scope
addFunction(name, enter, exit):
	Bind the name of a function to it's entry and exit points (instruction keys)
getFunctionPair(name):
	Get the (entry, exit) pair for a functoin name
addCallNode(node):
	Add a node as a call node
isCallNode(node):
	Check if a node is a call node
"""

# ----- #
# Frame #
# ----- #

class Frame(object):

	def __init__(self):
		super(Frame, self).__init__()
		self.subgraph = None
		self.functions = {}
		self.nodes = {}
		self.call = []

	def addSubGraph(self, enter, exit):
		self.subgraph = (enter, exit)
	def getSubGraphEntry(self):
		return self.subgraph[0]
	def getSubGraphExit(self):
		return self.subgraph[1]

	def addNode(self, node, inst):
		self.map.update({node : inst})
	def getInst(self, node):
		return self.map[node]

	def addFunction(self, name, enter, exit): 
		self.functions.update({name : (enter, exit)})
	def getFunctionPair(self, name): 
		return self.functions[name]
		
	def addCallNode(self, node):
		self.call += [node]
	def isCallNode(self, node):
		return node in self.call

# ------- #
# Scoping #
# ------- #

__STACK__ = []

def scope():
	global __STACK__
	__STACK__ += [Frame()]

def popScope():
	if len(__STACK__) > 1:
		global __STACK__
		__STACK__ = __STACK__[1:]

def getInst(node): 
	return __STACK__[0].getInst(node)
def addNode(node, inst): 
	__STACK__[0].addNode(node, inst)

def getSubGraphExit(): 
	return __STACK__[0].getSubGraphExit()
def getSubGraphEntry(): 
	return __STACK__[0].getSubGraphEntry()
def addSubGraph(enter, exit): 
	__STACK__[0].addSubGraph(enter, exit)

def isCallNode(node): 
	return __STACK__[0].isCallNode(node)
def addCallNode(node): 
	__STACK__[0].addCallNode(node)

def addFunction(name, enter, exit):
	__STACK__[0].addFunction(name, enter, exit)

def getFunctionPair(name):
	err = None
	for frame in __STACK__:
		try:
			pair = frame.getFunctionPair(name)
			return pair
		except KeyError:
			err = KeyError
	raise err
