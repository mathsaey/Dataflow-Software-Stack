# forin.py
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
# \package backEnd.DVM.forin
# \brief IGR for in structure changer
#
# This module contains functions to modify the IGR graph
# in order to be able to compile the for...in compound node.
##

import IGR
import IGR.node

##
# Stores the destination of the 
# context change for every split.
##
map = {}

##
# See how many arrays a for...in node 
# generates internally.
##
def getArrayCount(node):
	ctr = 0
	for port in node.subGraphs[1].exit.inputPorts:
		if port.isConnected():
			ctr += 1
	return ctr

##
# See if the generator accepts
# an array or creates on.
##
def acceptsArray(node):
	gen = node.subGraphs[0]
	if gen.entry in gen.nodes:
		return len(node.subGraphs[0].nodes) == 2
	else:
		return len(node.subGraphs[0].nodes) == 1

# --------------- #
# Return Subgraph #
# --------------- #

##
# Replace the subgraphHeader of the return subgraph with
# array instructions that will merge our inputs.
# We also update the map with the idx -> instruction mapping.
##
def addMerges(node):
	start = node.subGraphs[0].exit.inputs

	for port in node.subGraphs[2].entry.outputPorts[start:]:
		merge = IGR.createOperationNode(node.subGraphs[2], 'array')

		merge.getOutputPort(0).targets = port.targets
		port.targets = []

		for target in merge.getOutputPort(0).targets:
			target.source = merge.outputPorts[0]

		map.update({port.idx : [None, merge]})
	node.subGraphs[2].removeNode(node.subGraphs[2].entry)

# --------- #
# Generator #
# --------- #

def adjustGenerator(node):
	gen = node.subGraphs[0]

	# Remove the elements provided by scatter/range
	arrPort = gen.exit.getInputPort(node.inputs)
	dst = gen.exit.getInputPort(0)
	src = arrPort.source
	src.removeTarget(arrPort)
	arrPort.source = None
	
	# If we are dealing with a generated array
	# (instead of an external one, link the array
	# generator.
	if not acceptsArray(node):
		src.addTarget(dst)
		dst.source = src

	# Get the arguments to the node linked to the
	# exit node (which will lead to the split)
	for port in node.inputPorts:
		src = port.source
		idx = port.idx

		# Shift the elements to the right if we
		# had to generate our own array
		if not acceptsArray(node): idx += 1

		dst = gen.exit.getInputPort(idx)
		src.removeTarget(port)
		src.addTarget(dst)
		dst.attach(src)

		entryPort = gen.entry.getOutputPort(port.idx)
		targets = entryPort.targets
		entryPort.targets = []

		for target in targets: target.source = src
		src.addTargets(targets)	

	gen.removeNode(gen.entry)


# ---- #
# Body #
# ---- #

##
# Adjust the ports of the body so that the array
# elements are at port 0 and the other arguments after it.
##
def shiftBodyPorts(node):
	entry = node.subGraphs[1].entry
	arrIdx = node.inputs

	if acceptsArray(node):	
		oldArrPort = entry.getOutputPort(arrIdx)
		newArrPort = entry.getOutputPort(0)
	
		newArrPort.targets = oldArrPort.targets
		oldArrPort.targets = []

		for target in newArrPort.targets:
			target.source = newArrPort
	else:
		arrPort = entry.getOutputPort(arrIdx)
		entry.outputPorts[1:arrIdx + 1] = entry.outputPorts[:arrIdx]
		entry.outputPorts[0] = arrPort

		for idx in xrange(0, arrIdx + 1):
			entry.outputPorts[idx].idx = idx

##
# Follow the path through the body,
# starting from the exit point and 
# add every node we encounter up to the entry.
##
def duplicatePath(node, idx):
	sg = IGR.createCompoundSubGraph()
	sg.name = "body_%d" % idx
	node.subGraphs.append(sg)

	entryNode = node.subGraphs[1].entry
	bodyPort  = node.subGraphs[1].getInputPort(idx)
	copyPort  = sg.getInputPort(idx)
	bodyNode  = bodyPort.source.node
	lst       = [(bodyNode, bodyPort, copyPort)]

	while lst:
		bodyNode, bodyPort, copyPort = lst.pop()

		if bodyNode is entryNode: 
			IGR.connect(sg.entry, bodyPort.source.idx, copyPort.node, bodyPort.idx)
			continue

		copyNode = bodyNode.copy(sg)
		sg.addNode(copyNode)

		IGR.connect(copyNode, bodyPort.source.idx, copyPort.node, bodyPort.idx)

		for port in bodyNode.inputPorts:
			if port.acceptsLiteral():
				copyNode.getInputPort(port.idx).attach(port.source)
			else:
				lst.append((port.source.node, port, copyNode.getInputPort(port.idx)))

##
# Duplicate the path for every out port that produces
# an array.
##
def splitBody(node):
	if getArrayCount(node) == 1:
		idx = node.inputs + 1
		node.subGraphs[1].name = "body_%d" % idx
		node.subGraphs.append(node.subGraphs[1])
	else:
		for port in node.subGraphs[1].exit.inputPorts:
			if port.isConnected():
				duplicatePath(node, port.idx)

def addBodySinks(node):
	for sg in node.subGraphs[3:]:
		idx = int(sg.name[5:])
		arr = map[idx]
		arr[0] = sg.entry

# ------- #
# General #
# ------- #

def convertForIn(node):
	global map
	map = {}

	node.subGraphs[0].name = "Generate"
	node.subGraphs[2].name = "Return"

	adjustGenerator(node)	
	addMerges(node)

	shiftBodyPorts(node)
	splitBody(node)
	addBodySinks(node)

	node.map = map

def checkNode(node):
	if (isinstance(node, IGR.node.CompoundNode) and 
		node.type == 'forall'):
		convertForIn(node)

def convert():
	IGR.traverse(
		checkNode, 
		lambda x : None,
		lambda x : None,
		False,
		lambda x : None,
		lambda x : None
		)