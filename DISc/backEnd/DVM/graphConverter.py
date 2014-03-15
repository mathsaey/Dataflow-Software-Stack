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
##

import IGR
import dis
import converter

##
# Convert a collection of subGraphs
# to a DIS program.
#
# \param subGraphs
#		A list of subgraphs to compile.
# \param entryName
#		The name of the entry point in the program.
#		This subgraph will be linked to the entry and
#		exit of the DVM program.
##
def convert(subGraphs = IGR.getSubGraphs(), entryName = 'main'):
	main = IGR.getSubGraph(entryName).entry
	inputs = main.outputs
	prog = dis.DIS(inputs)
	nodes = []

	def node(n): 
		converter.convertNode(prog, n)
		nodes.append(n)

	def sgStart(sg): 
		for c in xrange(0, prog.chunks):
			prog.addCommentLine("Starting subgraph %s" % sg.name, c)

	def sgStop(sg):
		for c in xrange(0, prog.chunks):
			prog.addNewline(c)

		for node in nodes:
			converter.addLinks(prog, node)

		for c in xrange(0, prog.chunks):
			prog.addNewline(c)

		for node in nodes:
			converter.addLiterals(prog, node)

		for c in xrange(0, prog.chunks):
			prog.addCommentLine("Leaving subgraph %s" % sg.name, c)
			prog.addNewline(c)

		del nodes[:]

	def cmpStart(comp): pass
	def cmpStop(comp): pass

	IGR.traverse(
		node, sgStart, sgStop, 
		False, cmpStart, cmpStop, 
		subGraphs)

	# Add an implicit call to main, which returns to the 
	# program exit point.
	prog.addCommentLine("Implicit call to main", 0)
	mainKey = converter.getKey(main)
	mainCall = prog.addInstruction(0, 'CC', [mainKey[0], mainKey[1], 0, 1])
	prog.linkStart(mainCall)

	return prog.generate()