# AbstractNode.py
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
This module contains the top level node type
"""

class AbstractNode(object):
	def __init__(self,inputs, outputs, inputConstructor, outputConstructor):
		self.inputs				= [None] * inputs
		self.outputs			= [None] * outputs
		self.inputConstructor 	= inputConstructor
		self.outputConstructor 	= outputConstructor

		self.fillList(self.inputs, self.inputConstructor)
		self.fillList(self.outputs, self.outputConstructor)

	def __str__(self):
		return str(id(self))

	def getInput(self, idx):
		return self.getFromList(self.inputs, self.inputConstructor, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, self.outputConstructor, idx)

	def sendOutput(self, idx, output):
		self.getOutput(idx).receiveInput(output)

	def sendOutputs(self, outputs):
		for idx in xrange(0, len(self.outputs)):
			self.sendOutput(idx, outputs[idx])

	def reset(self):
		for el in self.inputs:
			el.clear()
		for el in self.outputs:
			el.clear()

	def fillList(self, lst, constructor):
		for idx in xrange(0, len(lst)):
			lst[idx] = constructor(self, idx)

	def getFromList(self, lst, constructor, idx):
		try:
			res = lst[idx]
		except IndexError:
			lst += [constructor(self, idx)]
			return self.getFromList(lst, constructor, idx)
		else:
			return res
	