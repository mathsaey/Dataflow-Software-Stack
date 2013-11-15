# Port.py
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
This file contains the various ports, in and outputs to nodes
"""

from receiver import Receiver

class Port(Receiver):
	""" Represents a port, a port contains the in- or output data of a node"""
	def __init__(self, node, idx):
		self.idx = idx
		self.node = node
		self.data = None
		self.fromLiteral = False

	def __str__(self):
		return "port " + str(self.idx) + " of node " + str(self.node)

	def idx(self): 		return self.idx
	def node(self): 	return self.node
	def value(self): 	return self.data
	def ready(self): 	return self.data is not None

	def receiveInput(self,input, fromLiteral):
		print "Port:", self, "accepted input:", input
		self.fromLiteral = fromLiteral
		self.data = input

	def clear(self):
		if not self.fromLiteral:
			self.data = None

	def follow(self):
		raise NotImplementedError("follow is an abstract method!")

class InputPort(Port):
	""" Represents a port that stores it's value until it's requested"""

	def __str__(self):
		return "Input " + super(InputPort, self).__str__()

	def receiveInput(self,input, fromLiteral = False):
		super(InputPort, self).receiveInput(input, fromLiteral)
		self.node.receiveInput(self.idx)

	def follow(self):
		return self.node.getOutputs()

class OutputPort(Port):	
	""" Represents a port that just forwards it's input right away"""
	def __init__(self, node, idx):
		super(OutputPort, self).__init__(node, idx)
		self.edges = []

	def __str__(self):
		return "Output " + super(OutputPort, self).__str__()

	def addEdge(self, edge):
		self.edges += [edge]
		if self.ready():
			edge.receiveInput(self.data)

	def sendOutput(self):
		for el in self.edges:
			el.receiveInput(self.data)

	def receiveInput(self,input, fromLiteral = False):
		super(OutputPort, self).receiveInput(input, fromLiteral)
		self.sendOutput()

	def follow(self):
		res = []
		for edge in self.edges:
			res += [edge.destination]
		return res

class TargetPort(Port):
	""" Represents a port with a dynamic target """
	def __init__(self, node, idx):
		super(TargetPort, self).__init__(node, idx)
		self.target = None

	def __str__(self):
		return "Target " + super(TargetPort, self).__str__()

	def setTarget(self, target):
		self.target = target
		if self.ready():
			target.receiveInput(self.data)

	def receiveInput(self, input, fromLiteral = False):
		super(TargetPort, self).receiveInput(input, fromLiteral)
		if self.target:
			self.target.receiveInput(self.data)