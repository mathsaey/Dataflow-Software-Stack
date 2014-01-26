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
# \file if1parser/graph.py
# \namespace if1parser.graph
# \brief Node parser
# 
# This module allows us to parse all of the 
# graph elements (compound nodes, nodes and subgraphs)
##

import environment
import operations
import type

import igr

# --------- #
# Constants #
# --------- #

# N <label> <operation code>
_n_label_idx 	= 1
_n_code_idx 	= 2

# G <type_reference> <name>
# X <type_reference> <name>
# I <type_reference> <name>
_g_type_idx		= 1
_g_name_idx		= 2

# { Compound <label> <operation code>
_cs_label_idx	= 2
_cs_code_idx  	= 3

# } <label> <operation code> <association list length> <association list>
_ce_label_idx	= 1
_ce_code_idx 	= 2
_ce_len_idx		= 3
_ce_lis_idx		= 4

# ------------ #
# Graph Parser #
# ------------ #

## Parse an IF1 subgraph.
def parseGraph(arr, ctr):
	name    = arr[_g_name_idx][1:-1]
	typeIdx = int(arr[_g_type_idx])
	sig     = type.getType(typeIdx)
	inputs  = len(sig.args.list)
	outputs = len(sig.res.list)

	graph = igr.createSubGraph(name, inputs, outputs)

	environment.popScope()
	environment.scope(graph)

# ----------- #
# Node Parser #
# ----------- #

def parseStandardNode(opCode):
	operation = operations.getFunction(opCode)
	return igr.createOperationNode(environment.getSubGraph(), operation)

def parseCallNode():
	return igr.createCallNode(environment.getSubGraph())

def parseNode(arr, ctr): 
	label  = int(arr[_n_label_idx])
	opCode = int(arr[_n_code_idx])
	node   = None

	if opCode is 120:
		node = parseCallNode()
	else:
		node = parseStandardNode(opCode)
	
	environment.addNode(label, node)
