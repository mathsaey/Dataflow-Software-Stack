# edge.py
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
# \package frontEnd.IF1.edge
# \brief Parse edges and literalss
# 
# This module is responsible for parsing 
# IF1 edges and literals and adding them to 
# the IGR.
##

import logging
log = logging.getLogger(__name__)

import IGR
import IGR.node

import environment
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

## Parse an IF1 edge 
def parseEdge(arr, ctr):
	srcLabel = int(arr[_e_src_idx])
	dstLabel = int(arr[_e_dst_idx])
	srcPort  = int(arr[_e_srcp_idx]) - 1
	dstPort	 = int(arr[_e_dstp_idx]) - 1
	srcNode  = environment.getNode(srcLabel)
	dstNode  = environment.getNode(dstLabel)

	IGR.connect(srcNode, srcPort, dstNode, dstPort)

# -------------- #
# Literal Parser #
# -------------- #

## Parse a literal string that represents a basic type
def _parseBasicLit(str, typ, ctr):
	if typ.type is int:
		return int(str)
	elif typ.type is bool:
		return str is "T"
	else:
		log.error("Line %d, Unsupported literal, %s encountered.", ctr, str)

## Parse a literal string.
def _parseLitStr(str, typ, ctr):
	string = str[1:-1] #strip enclosing ""
	if isinstance(typ, type._BasicType):
		return _parseBasicLit(string, typ, ctr)
	elif isinstance(typ, type._FunctionType):
		return string
	else:
		log.error("Line %d, Unsupported literal, %s encountered.", ctr, str)

## Parse an IF1 literal
def parseLiteral(arr, ctr):
	label   = int(arr[_l_dst_idx])
	port    = int(arr[_l_dstp_idx]) - 1
	typeKey = int(arr[_l_type_idx])
	string  = arr[_l_str_idx]

	node    = environment.getNode(label)
	typ     = type.getType(typeKey)
	val     = _parseLitStr(string, typ, ctr)

	IGR.addLiteral(val, node, port)