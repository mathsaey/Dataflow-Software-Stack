# graphConverter.py
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
# \package backEnd.DVM.graphconverter
# \brief IGR converter
#
# This module converts the entire graph
# into DVM.
#
# \todo
#	Clean this up 
#		- cleaner abstraction for not using first subgraph
#		- Type check for compound node type.
##

import IGR
import dis
import IGR.node
import converter

##
# Add the contents of a collection of subGraphs
# to a DIS program.
#
# \param subGraphs
#		A list of subgraphs to compile.
# \param prog
#		The DIS object to add the data to. 
##
def convertSubGraphs(subGraphs, prog):
	nodes = []

	def compStart(comp):
		prog.indent += 1

		retKey = prog.getFromKey(comp)
		for sg in comp.subGraphs[1:]:
			# Everything that links to exit node of sg will
			# now link to the common exit sink instead.
			prog.linkNode(sg.exit, retKey, retKey)
			if sg.exit in sg.nodes:
				# Make sure we don't parse exit node,
				# but keep it as attribute.
				sg.nodes.remove(sg.exit)

	def compStop(comp, idx):
		prog.indent -= 1

		dstLst = []
		for sg in comp.subGraphs[1:]:
			pair = prog.getToKey(sg.entry)
			dstLst.append(str(pair[0]))
			dstLst.append(str(pair[1]))
		prog.modifyString(0, idx, lambda str : str + ' '.join(dstLst))

	def nodeProc(node):
		converter.convertNode(prog, node)
		nodes.append(node)

		if node.isCompound():
			idx = prog.getIdx(0) - 1
			compStart(node)
			convertSubGraphs(node.subGraphs[1:], prog)
			compStop(node, idx)

	def sgStart(sg):
		prog.addCommentLines("Starting subgraph %s" % sg.name)

	def sgStop(sg):
		prog.addNewlines()

		for node in nodes:
			converter.addLinks(prog, node)
			converter.addLiterals(prog, node)

		prog.addCommentLines("Leaving subgraph %s" % sg.name)
		prog.addNewlines()

		del nodes[:]

	IGR.traverse(
		nodeProc, sgStart, sgStop, 
		True, lambda x : None, lambda x : None,
		subGraphs)

##
# Convert a collection of subGraphs
# to a DIS program.
#
# \param entryName
#		The name of the entry point in the program.
#		This subgraph will be linked to the entry and
#		exit of the DVM program.
##
def convert(entryName = 'main'):
	main = IGR.getSubGraph(entryName).entry
	inputs = main.outputs

	if inputs == 0:
		print main.subGraph.value
		return "TRIV <= %s" % main.subGraph.value

	prog = dis.DIS(inputs)
	convertSubGraphs(IGR.getSubGraphs(), prog)

	# Add an implicit call to main, which returns to the 
	# program exit point.
	prog.addCommentLine("Implicit call to main", 0)
	mainKey = prog.getToKey(main)
	mainCall = prog.addInstruction(0, 'CC', [inputs, 1,mainKey[0], mainKey[1], 0, 1])
	prog.linkStart(mainCall)

	return prog.generate()