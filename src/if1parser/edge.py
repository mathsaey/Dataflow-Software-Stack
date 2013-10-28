# edge.py
# Mathijs Saey
# dvm prototype

"""
IF1 edge parser.

This module is responsible for parsing edges and literals.
"""

import core.literal
import core.edge

import graph
import tools
import type

# ---------------- #
# Public functions #
# ---------------- #

def parseLiteral(arr, ctr): pass
def parseEdge(arr, ctr): pass

# --------- #
# Constants #
# --------- #

# E <source_node> <port> <destination_node> <port> <type>
_e_src_idx 		= 1
_e_srcp_idx 	= 2 
_e_dest_idx 	= 3
_e_destp_idx	= 4
_e_type_idx 	= 5

# L destination_node port type string 
_l_dest_idx		= 1
_l_destp_idx	= 2
_l_type_idx 	= 3
_l_str_idx		= 4

# ----------- #
# Edge Parser #
# ----------- #

def parseEdge(arr, ctr):
	srcKey 		= int(arr[_e_src_idx])
	srcPort 	= int(arr[_e_srcp_idx])
	destKey 	= int(arr[_e_dest_idx])
	destPort 	= int(arr[_e_destp_idx])

	src 	= graph.getNode(srcKey, ctr)
	dest 	= graph.getNode(destKey, ctr)
	sport 	= None
	dport 	= None

	if srcKey is 0:
		sport = src.getInput(srcPort - 1)
	else:
		sport = src.getOutput(srcPort - 1)
	if destKey is 0:
		dport = dest.getOutput(destPort - 1)
	else: 
		dport = dest.getInput(destPort - 1)
	core.edge.Edge(sport, dport)

# -------------- #
# Literal Parser #
# -------------- #

def parseBasicLit(str, typ, ctr):
	if typ.type is int:
		return int(str)
	elif typ.type is bool:
		return str is "T"
	else:
		err = "Unsupported literal, " + str + " encountered."
		tools.error(err,ctr)

def parseLitStr(str, typ, ctr):
	string = str[1:-1] #strip enclosing ""
	if isinstance(typ, type._BasicType):
		return parseBasicLit(string, typ, ctr)
	elif isinstance(typ, type._FunctionType):
		return string
	else:
		err = "Unsupported literal, " + str + " encountered."
		tools.error(err,ctr) 

def parseLiteral(arr, ctr):
	destKey	= int(arr[_l_dest_idx])
	portKey	= int(arr[_l_destp_idx])
	typeKey	= int(arr[_l_type_idx])
	string 	= arr[_l_str_idx]

	node = graph.getNode(destKey, ctr)
	port = node.getInput(portKey - 1)
	typ = type.getType(typeKey)

	val = parseLitStr(string, typ, ctr)
	core.literal.Literal(port, val)
