# port.py
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
This file defines ports, input acceptors for instructions
"""

class Port(object):
	def __init__(self, instruction, idx):
		super(Port, self).__init__()
		self.instruction = instruction
		self.token = None
		self.idx = idx
     
	def __str__(self):
		return "Port " + str(self.idx) + " of instruction " + str(self.instruction)

	def acceptToken(self, token):
		print self, "accepted input:", token
		self.token = token

	def isReady(self):
		return self.token is not None