# CompoundNode.py
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
This module contains the compound nodes, nodes that have subgraphs
"""

import copy

import edge
import port
import runtime

from abstractnode import AbstractNode
from executablenode import ExecutableNode

class CompoundNode(AbstractNode):
	"""A Compound node represents a more complex node that contains subgraphs"""

	def __init__(self, inputs, outputs, mergeNode):
		super(CompoundNode, self).__init__(inputs, outputs)
		self.fillList(self.outputs, port.OutputPort)
		self.fillList(self.inputs, port.OutputPort)
		self.mergeNode = mergeNode
		self.subgraphs = []

	def __str__(self):
		id = super(CompoundNode, self).__str__()
		return "CompoundNode: (" + id + ")"

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.OutputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

	def attach(self, subGraph, graphIdx):
		for idx in xrange(0, len(subGraph.outputs)):
			dst = self.mergeNode.getInput(idx, graphIdx)
			src = subGraph.getOutput(idx)
			edge.Edge(src, dst)
		for idx in xrange(0, len(subGraph.inputs)):
			dst = subGraph.getInput(idx)
			src = self.getInput(idx)
			edge.Edge(src, dst)

	def addSubGraphs(self, lst):
		mergeNode = self.mergeNode(
			len(self.inputs), 
			len(self.outputs), 
			len(lst))
		self.mergeNode = mergeNode
		self.subgraphs = lst
		for idx in xrange(0, len(lst)):
			el = lst[idx]
			self.attach(el, idx)

class MergeNode(ExecutableNode):

	def __init__(self, inputs, outputs, subgraphs):
		super(MergeNode, self).__init__(inputs, outputs)
		self.fillList(self.outputs, port.OutputPort)
		self.inputs = [None] * subgraphs

		for idx in xrange(0, subgraphs):
			lst = [None] * inputs
			self.fillList(lst, port.InputPort)
			self.inputs[idx] = lst

	def getInput(self, idx, graphIdx):
		return self.getFromList(self.inputs[graphIdx], port.InputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

class SelectNode(MergeNode):

	def __str__(self):
		id = super(SelectNode, self).__str__()
		return "SelectNode: (" + id + ")"

	def receiveInput(self, idx):
		if self.inputs[0][0].ready():
			self.select = self.inputs[0][0].value() + 1
			self.addToScheduler()

	def gatherInput(self):
		resLst = []
		for el in self.inputs[self.select]:
			resLst += [el.value()]
		return resLst

	def execute(self):
		res = self.gatherInput()
		self.sendOutputs(res)