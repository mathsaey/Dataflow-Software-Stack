# graph.py
# Mathijs Saey
# dvm prototype

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

"""
This module defines the functions that allow us to parse nodes and subgraphs
"""

import execution.api
import environment

import operations
import type

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

def parseGraph(arr, ctr):
	name = arr[_g_name_idx][1:-1]

	entry = execution.api.addForwardInstruction()
	exit = execution.api.addContextRestoreInstruction()

	environment.popScope()
	environment.addFunction(name, entry, exit)
	environment.scope()
	environment.addSubGraph(entry, exit)

# ----------- #
# Node Parser #
# ----------- #

def parseStandardNode(key, label):
	tuple 	  = operations.getFunction(key)
	operation = tuple[0]
	inputs    = tuple[1]

	inst = execution.api.addOperationInstruction(operation, inputs)
	environment.addNode(label, inst)

def parseCallNode(label):
	ret  = execution.api.addForwardInstruction()
	inst = execution.api.addContextChangeInstruction(ret)
	environment.addNode(label, inst)
	environment.addNode(-label, ret)
	environment.addCallNode(label)

def parseNode(arr, ctr): 
	key 		= int(arr[_n_code_idx])
	label 		= int(arr[_n_label_idx])

	if key is 120:
		parseCallNode(label)
	else:
		parseStandardNode(key, label)
