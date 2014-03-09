# literals.py
# Mathijs Saey
# DISc

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

##
# \package traversals.literals
# \brief IGR Literal removal
# 
# This module defines a few traversals
# that remove literals from the IGR where
# possible.
##

import dvm
import dis
import traverse
import IGR.node


def isLiteral(node):
	if isinstance(node, IGR.node.OperationNode):
		for port in node.inputPorts:
			if not port.acceptsLiteral():
				return False
		return True

def getInputs(node):
	res = []
	for port in node.inputPorts:
		res.append(port.source.value)
	return res

def getValue(node):
	inputs = getInputs(node)
	prog = dis.DIS(node.inputs)
	prog = repr(prog)
	val = dvm.run(dis = prog, inputs = inputs)
	return val

def transformNode(node, value): 
	for port in node.outputPorts:
		for port in port.targets:
			port.attach(value)

def deleteNode(node):
	sg = node.subGraph
	sg.nodes.remove(node)

def removeOperationLiterals():


	traverse.traverseAll(
		checkNode,
		lambda x: None,
		lambda x: None,
		False,
		lambda x: None,
		lambda x: None
		)