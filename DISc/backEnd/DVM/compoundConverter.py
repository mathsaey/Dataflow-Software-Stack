# compoundConverter.py
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
# \package backEnd.DVM.compoundConverter
# \brief IGR compound node compiler
#
# This module contains functions for the compilation of compound nodes.
# It's worth noting that the links to and from a compound node are made by
# the regular nodeConverter.
##

import graphConverter

# ----------- #
# Select Node #
# ----------- #

##
# Ensure all the subgraphs
# link to the exit sink.
##
def selectStart(dis, comp):
	dis.indent += 1

	retKey = dis.getFromKey(comp)
	for sg in comp.subGraphs[1:]:
		# Everything that links to exit node of sg will
		# now link to the common exit sink instead.
		dis.linkNode(sg.exit, retKey, retKey)
		if sg.exit in sg.nodes:
			# Make sure we don't parse exit node,
			# but keep it as attribute.
			sg.nodes.remove(sg.exit)

##
# Add all the subgraph entry points
# to the destination list of select.
##
def selectStop(dis, comp, idx):
	dis.indent -= 1

	dstLst = []
	for sg in comp.subGraphs[1:]:
		pair = dis.getToKey(sg.entry)
		dstLst.append(str(pair[0]))
		dstLst.append(str(pair[1]))
	dis.modifyString(0, idx, lambda str : str + ' '.join(dstLst))

##
# Convert a select node.
#
# First, we add the node itself to dis.
# We add a sink and a switch. The switch is the
# actual select while the sink will be the exit point
# of any results coming out of the compound node.
#
# We register the switch as the destination for any incoming links
# while the sink is registered as the source of outgoing links.
#
# Next, we simply ensure all the subgraphs link to the shard sink,
# and compile the subgraphs.
#
# Finally, we get the dis addresses of the possible destinations, after
# which we add them to the destination list of the switch node.
##
def convertSelectNode(dis, node):
	switch = dis.addInstruction(0, 'SWI', [])
	sink   = dis.addInstruction(0, 'SNK', [])
	dis.linkNode(node, switch, sink)

	idx = dis.getIdx(0) - 1
	selectStart(dis, node)
	graphConverter.convertSubGraphs(node.subGraphs[1:], dis)
	selectStop(dis, node, idx)

# ---------- #
# Forin Node #
# ---------- #

def convertForAllNode(dis, node):
	dis.addNewlines()
	dis.addCommentLines("Starting for...in")
	bgn = dis.addInstruction(0, 'SNK', [])
	end = dis.addInstruction(0, 'SNK', [])
	dis.linkNode(node, bgn, end)

	dis.indent += 1

	inputs = node.inputs + 1

	splits = [dis.addInstruction(1, 'SPL', [inputs]) for e in node.map]
	stopIdx = dis.getIdx(1)
	startIdx = stopIdx - len(node.map) + 1

	for key in splits:
		for i in xrange(0, inputs):
			dis.addLink(bgn, i, key, i)

	gen = node.subGraphs[0]
	dis.linkNode(gen.exit, bgn, bgn)
	gen.removeNode(gen.exit)
	graphConverter.convertSubGraphs(node.subGraphs[0:1], dis)

	graphConverter.convertSubGraphs(node.subGraphs[3:], dis)

	ret = node.subGraphs[2]
	dis.linkNode(ret.exit, end, end)
	ret.removeNode(ret.exit)
	graphConverter.convertSubGraphs(node.subGraphs[2:3], dis)

	for key, idx in zip(node.map,xrange(startIdx, stopIdx + 1)):
		sink, merge = node.map[key]
		dstChunk, dstInst = dis.getToKey(sink)
		mergeChunk, mergeInst = dis.getToKey(merge)

		dis.modifyString(1, idx, 
			lambda str : str + " %s %s %s %s" % 
			(dstChunk, dstInst, mergeChunk, mergeInst))

	dis.indent -= 1

# ------- #
# General #
# ------- #

converters = {
	'select' : convertSelectNode,
	'forall' : convertForAllNode
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
##
def convertNode(dis, node):
	return converters[node.type](dis, node)