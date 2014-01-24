# edge.py
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
This module is responsible for parsing edges and literals.
"""

import execution.api

import environment
import tools
import type

# --------- #
# Constants #
# --------- #

# E <source_node> <port> <destination_node> <port> <type>
_e_src_idx  = 1
_e_srcp_idx = 2 
_e_dst_idx  = 3
_e_dstp_idx = 4
_e_type_idx = 5

# L destination_node port type string 
_l_dst_idx  = 1
_l_dstp_idx	= 2
_l_type_idx = 3
_l_str_idx  = 4

# ----------- #
# Edge Parser #
# ----------- #

def parseEdge(arr, ctr):
	srcNode 	= int(arr[_e_src_idx])
	srcPort 	= int(arr[_e_srcp_idx])
	dstNode 	= int(arr[_e_dst_idx])
	dstPort 	= int(arr[_e_dstp_idx])

	src 	= None
	dst 	= None

	if srcNode is 0: src = environment.getSubGraphEntry()
	else: src = environment.getInst(srcNode)
	if dstNode is 0 : dst = environment.getSubGraphExit()
	else: dst = environment.getInst(dstNode)

	if environment.isCallNode(srcNode):
		srcPort = srcPort - 1
		src = environment.getInst(-srcNode)
	if environment.isCallNode(dstNode): dstPort = dstPort - 1

	execution.api.addDestination(src, srcPort - 1, dst, dstPort - 1)

# -------------- #
# Literal Parser #
# -------------- #

def _parseBasicLit(str, typ, ctr):
	if typ.type is int:
		return int(str)
	elif typ.type is bool:
		return str is "T"
	else:
		err = "Unsupported literal, " + str + " encountered."
		tools.error(err,ctr)

def _parseLitStr(str, typ, ctr):
	string = str[1:-1] #strip enclosing ""
	if isinstance(typ, type._BasicType):
		return _parseBasicLit(string, typ, ctr)
	elif isinstance(typ, type._FunctionType):
		return string
	else:
		err = "Unsupported literal, " + str + " encountered."
		tools.error(err,ctr) 

def _parseFunctionName(inst, str, ctr):
	funcPair = environment.getFunctionPair(str)
	execution.api.bindCall(inst, funcPair[0], funcPair[1])

def parseLiteral(arr, ctr):
	key	    = int(arr[_l_dst_idx])
	port    = int(arr[_l_dstp_idx])
	typeKey = int(arr[_l_type_idx])
	string  = arr[_l_str_idx]

	typ = type.getType(typeKey)
	val = _parseLitStr(string, typ, ctr)

	inst = None

	if key is 0: inst = environment.getSubGraphExit()
	else: inst = environment.getInst(key)

	if environment.isCallNode(key):
		if (port is 1):
			_parseFunctionName(inst, val, ctr)
			return
		else:
			port = port - 1

	execution.api.addLiteral(inst, port - 1, val)