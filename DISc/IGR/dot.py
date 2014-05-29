# dot.py
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
# \package IGR.dot
# \brief IGR dot parser
# 
# This module can return a dot version of the graph.
# Mainly useful for debugging the compilation process.
##

import traverse

import StringIO
import subprocess

import logging
log = logging.getLogger(__name__)

# --------- #
# Subgraphs #
# --------- #

##
# Add the attributes of the subgraph.
##
def subGraphHeader(buffer, subGraph):
	name = subGraph.name.replace(".", "_")
	buffer.write("subgraph cluster_" + name + " {\n")
	buffer.write("label = " + name + "\n")
	buffer.write("graph [pencolor = black, bgcolor = white]\n")

## "close" the subgraph.
def subGraphFooter(buffer, subGraph):
	buffer.write("}\n")

# -------- #
# Compound #
# -------- #

def compoundHeader(buffer, node):
	name = str(node.key)
	buffer.write("subgraph cluster_compound_" + name + " {\n")
	buffer.write("label = compound_" + name + "\n")
	buffer.write("graph [pencolor = black, bgcolor = lightgrey]\n")

def compoundFooter(buffer, node):
	buffer.write("}\n")

# ----- #
# Ports #
# ----- #

##
# Get a representation for a port.
#
# \return 
# 		Return the value of the literal, if this port
#		accepts a literal. * if this port is connected to
#		another port. Returns the empty string if this port
#		is not connected to anything
##
def portString(port, preFix = ""):
	if port.acceptsLiteral(): return str(port.source.value)
	elif port.isConnected():  return "<" + preFix + str(port.idx) + ">" + " *"
	else: return "<" + preFix + str(port.idx) + ">"

##
# String representation of a port list.
#
# \param portLst
#		The list with ports, should not be None
#
# \return 
# 		Returns a string that will show the values of all the ports
# 		in a horizontal line when parsed by dot.
# 		Returns the empty string if the portLst is None
##
def ports(portLst, prefix = ""):
	res = ""
	for port in portLst:
		res += "|" + portString(port, prefix)
	return "{" + res[1:] + "}"

## Get the portlist for the inputs of a node.
def inputList(node):
	if node.inputPorts:
		return ports(node.inputPorts, "I") + "|"
	else: return ""

## Get the portlist for the outputs of a node.
def outputList(node):
	if node.outputPorts:
		return "|" + ports(node.outputPorts, "O")
	else: return ""

# ----- #
# Nodes #
# ----- #

## Identifier of the node.
def nodeIdentifier(node):
	return str(node.key)

## Convert a connection to a string
def edgeStr(srcNode, scrPort, dstNode, dstPort):
	src = nodeIdentifier(srcNode) + " : O" + str(scrPort) 
	dst = nodeIdentifier(dstNode) + " : I" + str(dstPort)
	return src + " -> " + dst + ";"

## Add the label of the node to the buffer. 
def nodeLabel(buffer, node):
	buffer.write(nodeIdentifier(node))
	buffer.write(' [')
	buffer.write('label="' + '{' + inputList(node) + str(node) + outputList(node) + '}"')
	if node.isCompound(): buffer.write("style = filled, fillcolor = lightgrey")
	if node.isCall(): buffer.write("style = dashed")
	buffer.write('];\n')

## Add all the outgoing edges of a node to the buffer.
def nodeLinks(buffer, node):
	if node.hasNext():
		for port in node.outputPorts:
			for target in port.targets:
				buffer.write(edgeStr(node, port.idx, target.node, target.idx) + "\n")

## Write the information of a node to the buffer
def node(buffer, node):
	nodeLabel(buffer, node)
	nodeLinks(buffer, node)

# --- #
# Dot #
# --- #

## Write general dot information
def dotHeader(buffer):
	buffer.write("digraph IGR {\n")
	buffer.write("graph [compound=true, dpi = 300];\n")
	buffer.write("node [shape=record];\n")

## Close the dot graph
def dotFooter(buffer):
	buffer.write("}")

## Create the dot string
def getDot(skipCompound):
	buffer = StringIO.StringIO()
	dotHeader(buffer)

	traverse.traverse(
		lambda nd: node(buffer, nd),
		lambda sg: subGraphHeader(buffer, sg),
		lambda sg: subGraphFooter(buffer, sg),
		skipCompound,
		lambda nd: compoundHeader(buffer, nd),
		lambda nd: compoundFooter(buffer, nd)
	)

	dotFooter(buffer)
	str = buffer.getvalue()
	buffer.close()
	return str

##
# Get the dot representation and 
# write it to a file.
##
def dotToFile(path, skipCompound = True):
	f = open(path, 'w')
	f.write(getDot(skipCompound))
	f.close()

##
# Convert the IGR graph to dot, save it,
# and run dot on this file. 
#
# This function should be call with keyword arguments.
# The default arguments will cause the following behaviour:
# 		* dot is assumed to be in your PATH.
#		* the dot file will be saved in igr.dot
#		* the output will be in png format.
#		* dot will decide where to store the output.
#			With the default settings this would be in igr.dot.png
#
# \param dotpath
#		The path of the dot executable, in case it's not in your PATH
# \param path
#		The location where the dot file will be stored.
# \param format
#		The output format of the graph dot creates from the dot file.
# \param output
#		The location where we store the output of dot.
#		Leaving this blank will pass the -O option.
#		The -O option let's dot choose the path.
# \param other
#		Any other options you want to pass to doth.
#		These options should be passed as a list of strings.
# \param skipCompound 
#		True if you do not want to display the compound nodes.
##
def dot(
	dotpath = "dot",
	path = "igr.dot", 
	format = "png", 
	output = "", 
	other = [], 
	skipCompound = True
	):

	dotToFile(path, skipCompound)

	format = "-T" + format

	if output: output = "-o" + output
	else: output = "-O"

	try:
		subprocess.check_call([dotpath, format, path, output] + other)
	except subprocess.CalledProcessError, e:
		log.error("Dot returned with exit code %d", e.returncode)
	except OSError:
		log.error("Dot executable not found")
