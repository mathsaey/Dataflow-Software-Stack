# nodeConverter.py
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
# \package backEnd.DVM.nodeConverter
# \brief IGR node converter
# 
# This module can convert the various IGR
# node types into an equivalent DIS statement.
##

import IGR.node

##
# Store the keys that
# nodes have received.
#
# Stored with the node key as
# key and the (chunk, inst) tuple
# as value.
##
nodes = {}

## Add the DIS version of an operation to a DIS object
def convertOpNode(dis, node):
	key = dis.addInstruction(1, 'OP', [node.operation, node.inputs])
	nodes.update({node.key : key})
	return key

def convertSGEntryNode(dis, node): pass

converters = {
	IGR.node.SubGraphEntryNode : convertSGEntryNode,
	IGR.node.OperationNode     : convertOpNode
}

##
# Add the DIS equivalent of a certain node
# to a DIS object.
#
# \param dis
#		A DIS instance that will contain the DIS version
#		of the node.
# \param node
#		The node to convert.
#
# \return The key of the node in DIS.
##
def convertNode(dis, node):
	return converters[type(node)](dis, node)