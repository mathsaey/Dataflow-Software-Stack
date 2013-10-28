# OperationNode.py
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
This module contains nodes that perform an operation on the data they receive
"""

from executablenode import ExecutableNode
import port

class OperationNode(ExecutableNode):
	def __init__(self, inputs, outputs, operation):
		super(OperationNode, self).__init__(inputs, outputs)
		self.fillList(self.outputs, port.OutputPort)
		self.fillList(self.inputs, port.InputPort)
		self.operation = operation

	def __str__(self):
		id = super(OperationNode, self).__str__()
		return "OperationNode: (" + id + ")"

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.InputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

	def receivedInput(self, idx):
		if self.isInputReady():
			self.addToScheduler()

	def gatherInput(self):
		resLst = []
		for el in self.inputs:
			resLst += [el.value()]
		return resLst

	def execute(self):
		super(OperationNode, self).execute()
		lst = self.gatherInput()
		res = self.operation(*lst)
		self.sendOutputs([res])
		self.reset()

