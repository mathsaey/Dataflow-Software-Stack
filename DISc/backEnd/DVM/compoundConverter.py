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
# \brief IGR compound node
#
# This module contains functions for the compilation of compound nodes.
# It's worth noting that the links to and from a compound node are made by
# the regular nodeConverter.
##

import graphConverter

# ----------- #
# Select Node #
# ----------- #

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

def selectStop(dis, comp, idx):
	dis.indent -= 1

	dstLst = []
	for sg in comp.subGraphs[1:]:
		pair = dis.getToKey(sg.entry)
		dstLst.append(str(pair[0]))
		dstLst.append(str(pair[1]))
	dis.modifyString(0, idx, lambda str : str + ' '.join(dstLst))


def convertSelectNode(dis, node):
	switch = dis.addInstruction(0, 'SWI', [])
	sink   = dis.addInstruction(0, 'SNK', [])
	dis.linkNode(node, switch, sink)

	idx = dis.getIdx(0) - 1
	selectStart(dis, node)
	graphConverter.convertSubGraphs(node.subGraphs[1:], dis)
	selectStop(dis, node, idx)

# ------- #
# General #
# ------- #

converters = {
	'select' : convertSelectNode
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