# graph.py
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
# \package IGR.graph
# \brief Complete program
# 
# This defines the complete program graph. All of the subgraphs
# as well as their names can be found here.
#
# This file also defines a few top level functions that 
# facilitate adding nodes, ports and literals to the IGR.
##

## All of the functions in the program 
__SUBGRAPHS__ = []

## The function names, combined with the subgraph they map to.
__FUNCTION_NAMES__ = {}

##
# Add a subgraph to the program.
#
# \param subGraph
#		The subgraph to add.
## 
def addSubGraph(subGraph):
	__SUBGRAPHS__.append(subGraph)

##
# Add a subgraph to a given name.
#
# \param graph
#		The graph to add. It's name 
#		field will be used to retrieve it.
##
def bindName(graph):
	__FUNCTION_NAMES__.update({graph.name : graph})

##
# Get a list of all the non-compound subgraphs
# in the program.
#
# \return 
#	 	All the non compound subgraphs in the program.
## 
def getSubGraphs():
	return __SUBGRAPHS__

##
# Get a subgraph by name.
#
# \param name
#		The name of the subgraph 
# 		we want to retrieve.
# \return
#		The subgraph
##
def getSubGraph(name):
	return __FUNCTION_NAMES__[name]