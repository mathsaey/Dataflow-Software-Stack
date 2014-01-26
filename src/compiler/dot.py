# dot.py
# Mathijs Saey
# dvm

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
# \file compiler/dot.py
# \namespace compiler.dot
# \brief IGR dot parser
# 
# This module can return a dot version of the graph.
##

import traverse

import StringIO
import subprocess

# --------- #
# Subgraphs #
# --------- #

##
# Generate a string for the start of a subgraph.
##
def sgStart(subGraph):
	return "subgraph cluster_" + subGraph.name + " {\n"

##
# Generate a string for the end of a subgraph.
##
def sgEnd():
	return "}\n"

# ----- #
# Nodes #
# ----- #

##
# Get a string key for the node.
##
def nodeKey(node):
	return str(node.key)

def nodeInputs(node):
	res = ""
	for port in node.inputPorts:
		if port.source.isPort():
			res += "|"
		else:
			res += "| " + str(port.source.value)
	return res[1:]

##
# Get the node label.
## 
def nodeLabel(node):
	if node.inputs is 0:
		inputs = ""
	else:
		inputs = "{" + nodeInputs(node) + "}|"
	if node.outputs is 0:
		outputs = ""
	else:
		outputs = "|{" + (node.outputs * "|")[1:] + "}"

	title   = str(node)
	return '{' + inputs + title + outputs + '}' 

##
# String representation of a connection between nodes.
##
def edgeStr(src, dst):
	return nodeKey(src) + " -> " + nodeKey(dst) + ";"

##
# Get all the outgoing edges of a node.
##
def nodeLinks(node):
	links = ""
	if node.hasNext():
		for ports in node.outputPorts:
			for port in ports.targets:
				links += edgeStr(node, port.node) + "\n"
	return links

##
# Convert a node to a string
##
def nodeStr(node):
	desc = str(node.key) + ' [label="' + nodeLabel(node) + '"];\n'
	link = nodeLinks(node)
	return desc + link

# --- #
# Dot #
# --- #

##
# Get the dot string for the graph.
##
def getDot():
	res = StringIO.StringIO()
	res.write("digraph G {\n")
	res.write("graph [compound=true];\n")
	res.write("node [shape=record];\n")

	def subGraphStart(sg):
		res.write(sgStart(sg))
	def subGraphStop(sg):
		res.write(sgEnd())
	def nodeProc(n):
		res.write(nodeStr(n))

	traverse.traverseAllNodes(subGraphStart, subGraphStop, nodeProc)
	res.write("}")
	dot = res.getvalue()
	res.close()
	return dot

##
# Get the dot representation and 
# write it to a file.
##
def dotToFile(path):
	f = open(path, 'w')
	f.write(getDot())

##
# Get the dot representation,
# write it to a file and run dot on it.
# Requires dot to be in your path.
#
# Will store the output in png format.
# The image will be stored as <path>.png
##
def runDot(path):
	dotToFile(path)
	subprocess.call(["dot", "-Tpng", path, "-O"])
