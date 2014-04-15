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
# \brief IGR graph converter
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
import nodeConverter
import compoundConverter

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

	def nodeProc(node):
		if node.isCompound():
			compoundConverter.convertNode(prog, node)
		else:
			nodeConverter.convertNode(prog, node)
		nodes.append(node)

	def sgStart(sg):
		prog.addCommentLines("Starting subgraph %s" % sg.name)

	def sgStop(sg):
		prog.addNewlines()

		for node in nodes:
			nodeConverter.addLinks(prog, node)
		for node in nodes:
			nodeConverter.addLiterals(prog, node)

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
		return "TRIV <= %s" % main.subGraph.value

	prog = dis.DIS(inputs)
	convertSubGraphs(IGR.getSubGraphs(), prog)

	# Add an implicit call to main, which returns to the 
	# program exit point.
	prog.addCommentLine("Implicit call to main", 0)
	mainKey = prog.getToKey(main)
	mainCall = prog.addInstruction(0, 'CHN', [inputs, 1,mainKey[0], mainKey[1], 0, 1])
	prog.linkStart(mainCall)

	return prog.generate()