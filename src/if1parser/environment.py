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
getSubGraphExit(node):
	Get the instruction key the exit of node
getSubGraphEntry(node): 
	Get the instruction key matching the entry of node
addSubGraph(node, enter):
	Add the entry and exit instructions matching node
addFunction(name, enter, exit):
	Bind the name of a function to it's entry and exit points (instruction keys)
getFunctionEntry(name):
	Get the entry point of a function from it's name
getFunctionExit(name): 
	Get the exit point of a functoin from it's name
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
		self.functions = {}
		self.nodes = {}
		self.call = []

	def addNode(self, node, inst):
		self.map.update({node : inst})
	def addSubGraph(self, node, enter, exit):
		self.map.update({node : (enter, exit)})
	def getInst(self, node):
		return self.map[node]
	def getSubGraphEntry(self, node):
		return self.map[node][0]
	def getSubGraphExit(self, node):
		return self.map[node][1]
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
	global __STACK__
	frame = __STACK__[0]
	__STACK__ = __STACK__[1:]
	return frame

def getInst(node): 
	return __STACK__[0].getInst(node)
def addNode(node, inst): 
	__STACK__[0].addNode(node, inst)

def getSubGraphExit(node): 
	return __STACK__[0].getSubGraphExit(node)
def getSubGraphEntry(node): 
	return __STACK__[0].getSubGraphEntry(node)
def addSubGraph(node, enter): 
	__STACK__[0].addSubGraph(node, enter, exit)

def isCallNode(node): 
	return __STACK__[0].isCallNode(node)
def addCallNode(node): 
	__STACK__[0].addCallNode(node)

def addFunction(name, enter, exit):
	__STACK__[0].addFunction(name, enter, exit)

def _getFunctionPair(name):
	err = None
	for frame in __STACK__:
		try:
			pair = frame.getFunctionPair(name)
			return pair
		except KeyError:
			err = KeyError
	raise err

def getFunctionEntry(name):
	return _getFunctionPair(name)[0]
def getFunctionExit(name):
	return _getFunctionPair(name)[1]
