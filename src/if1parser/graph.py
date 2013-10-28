# graph.py
# Mathijs Saey
# dvm prototype

# The MIT License (MIT)
#
# Copyright (c) 2013 Mathijs Saey
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

import core.operationnode
import core.compoundnode
import core.functionnode
import core.callnode
import core.runtime

import operations
import tools
import type

# ---------------- #
# Public functions #
# ---------------- #

def parseCompoundStart(arr, ctr): pass
def parseCompoundEnd(arr, ctr): pass
def parseGraph(arr, ctr): pass
def parseNode(arr, ctr): pass
def getNode(key, ctr): pass

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

# ------- #
# Scoping #
# ------- #

class _Scope(object):
	""" Represents a single scope"""

	def __init__(self, collection):
		super(_Scope, self).__init__()
		self.map = collection

	def addEl(self):
		raise NotImplementedError("addEl is an abstract method!")

	def getEl(self, key):
		try:
			res = self.map[key]
		except KeyError:
			return None
		else:
			return res

class _NodeScope(_Scope):
	def __init__(self):
		super(_NodeScope, self).__init__({})

	def addEl(self, key, node):
		self.map.update({int(key): node})

class _SequentialScope(_Scope):
	def __init__(self):
		super(_SequentialScope, self).__init__([])

	def addEl(self, node):
		self.map += [node]

class _Environment(object):
	""" 
	An environment represents the current execution environment.
	It keeps track of the scoping rules when looking up nodes.
	"""
	def __init__(self, scopeType):
		super(_Environment, self).__init__()
		self.scopeType = scopeType
		self.stack = []
		self.level = 0
		self.stack.append(self.scopeType())

	def addScope(self):
		self.stack.append(self.scopeType())
		self.level += 1

	def popScope(self):
		if self.level is not 0:
			self.stack.pop()
			self.level -= 1

	def addEl(self, *args):
		self.stack[-1].addEl(*args)

	def getEl(self, key, ctr):
		res = None
		for el in reversed(self.stack):
			res = el.getEl(key)
			if res:
				break
		if res:
			return res
		else:
			err = "Undefined label: " + str(key)
			tools.error(err,ctr)

# ----- #
# State #
# ----- #

_COMP_LEVEL = 0
_nodes 		= _Environment(_NodeScope)
_subgraphs 	= _Environment(_SequentialScope)

# ------------ #
# Abstractions #
# ------------ #

def isCompound():
	return _COMP_LEVEL is 0
def addFunction(key, node):
	core.runtime.pool.addFunction(key, node)

def nodeScope():
	_nodes.addScope()
def nodePop():
	_nodes.popScope()
def addNode(key, node):
	_nodes.addEl(key, node)
def getNode(key, ctr = "?"):
	return _nodes.getEl(key, ctr)

def enterComp():
	global _COMP_LEVEL
	_COMP_LEVEL += 1
	_subgraphs.addScope()
def exitComp():
	global _COMP_LEVEL
	_COMP_LEVEL -= 1
	_subgraphs.popScope()

def addSubGraph(graph):
	_subgraphs.addEl(graph)
def getSubGraph(idx, ctr = "?"):
	return _subgraphs.getEl(idx, ctr)

# ------------ #
# Graph Parser #
# ------------ #

def parseNormalGraph(arr, ctr):
	typeIdx = int(arr[_g_type_idx])
	sig = type.getType(typeIdx)
	inputs = len(sig.args.list)
	outputs = len(sig.res.list)

	node = core.functionnode.FunctionNode(inputs, outputs)
	name = arr[_g_name_idx][1:-1]
	nodePop()
	addFunction(name, node)
	nodeScope()
	addNode(0, node)

def parseSubGraph(arr, ctr):
	node = core.functionnode.FunctionNode(0,0)
	addSubGraph(node)
	nodePop()
	nodeScope()
	addNode(0, node)

def parseGraph(arr, ctr):
	if _COMP_LEVEL is 0:
		parseNormalGraph(arr, ctr)
	else:
		parseSubGraph(arr, ctr)

def parseGraphDef(arr, ctr):
	pass

# --------------- #
# Compound Parser #
# --------------- #

def parseCompoundStart(arr, ctr):
	opCode = arr[_cs_code_idx]
	const = operations.getCompound(opCode)
	node = const()

	enterComp()
	addNode(0, node)
	nodeScope()
	nodeScope()


def parseCompoundEnd(arr, ctr):
	nodePop()
	node 	= getNode(0, ctr)
	label 	= arr[_ce_label_idx]
	length	= int(arr[_ce_len_idx])
	end 	= _ce_lis_idx + length
	lst 	= arr[_ce_lis_idx:end]
	resLst 	= []

	for idx in xrange(0, len(lst)):
		graphIdx = lst[idx]
		graph = getSubGraph(idx, ctr)
		resLst += [graph]

	node.addSubGraphs(resLst)
	addNode(label, node)
	exitComp()

# ----------- #
# Node Parser #
# ----------- #

def parseStandardNode(key, label):
	operation 	= operations.getFunction(key)
	inputs		= operation.func_code.co_argcount
	outputs 	= 1

	node = core.operationnode.OperationNode(inputs, outputs, operation)
	addNode(label, node)

def parseCallNode(label):
	node = core.callnode.CallNode(1,1)
	addNode(label, node)

def parseNode(arr, ctr): 
	key 		= int(arr[_n_code_idx])
	label 		= int(arr[_n_label_idx])

	if key is 120:
		parseCallNode(label)
	else:
		parseStandardNode(key, label)
