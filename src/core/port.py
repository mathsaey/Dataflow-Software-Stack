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

from dataconnector import DataConnector

class Port(DataConnector):
	""" Represents a port, a port contains the in- or output data of a node"""
	def __init__(self, node, idx, typ = "Unknown"):
		self.idx = idx
		self.typ = typ
		self.node = node
		self.input = None
		self.fromLiteral = False

	def __str__(self):
		return self.typ + " port " + str(self.idx) + " of node " + str(self.node)

	def value(self):
		return self.input

	def node(self):
		return self.node

	def acceptInput(self,input, fromLiteral):
		print "Port:", self, "accepted input:", input
		self.fromLiteral = fromLiteral
		self.input = input

	def ready(self):
		return self.input is not None

	def clear(self):
		if not self.fromLiteral:
			self.input = None

class InputPort(Port):
	""" Represents a port that keeps it's input until the node is ready"""
	def __init__(self, node, idx, typ = "Input"):
		super(InputPort, self).__init__(node, idx, typ)

	def acceptInput(self,input, fromLiteral = False):
		super(InputPort, self).acceptInput(input, fromLiteral)
		self.node.receivedInput(self.idx)

class OutputPort(Port):	
	""" Represents a port that just forwards it's input right away """
	def __init__(self, node, idx, typ = "Output"):
		super(OutputPort, self).__init__(node, idx, typ)
		self.edges = []

	def addEdge(self, edge):
		self.edges += [edge]
		if self.ready():
			edge.acceptInput(self.input)

	def sendOutput(self):
		for el in self.edges:
			el.acceptInput(self.input)

	def acceptInput(self,input, fromLiteral = False):
		super(OutputPort, self).acceptInput(input, fromLiteral)
		self.sendOutput()

class StopPort(OutputPort):
	""" Represents an output port that only forwards it's input when told """
	def __init__(self, node, idx, typ = "Stop"):
		super(StopPort, self).__init__(node, idx, typ)
		self.activated = False

	def addEdge(self, edge):
		super(StopPort, self).addEdge(edge)

	def acceptInput(self, input, fromLiteral = False):
		super(OutputPort, self).acceptInput(input, fromLiteral)
		self.node.receivedInput(self.idx)
		if (self.activated):
			self.sendOutput()

	def activate(self):
		self.activated = True
		if self.input:
			self.sendOutput()
