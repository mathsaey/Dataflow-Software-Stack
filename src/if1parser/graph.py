# graph.py
# Mathijs Saey
# dvm prototype

import core.operationnode
import core.functionnode
import core.callnode
import core.runtime

import operations
import tools
import type

"""
IF1 Graph parser

This module defines the functions that allow us to parse nodes, 
edges and functions.
"""

# ---------------- #
# Public functions #
# ---------------- #

def parseNode(arr, ctr): pass
def envGet(key, ctr): pass

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

# ----- #
# State #
# ----- #

__PARSING_COMPOUND = 0

# ------- #
# Scoping #
# ------- #

class _Scope(object):
	"""
	A scope represents a single level of node definitions. 
	"""

	def __init__(self):
		super(_Scope, self).__init__()
		self.map = {}

	def addEl(self, key, node):
		self.map.update({key: node})

	def getEl(self, key):
		try:
			res = self.map[key]
		except KeyError:
			return None
		else:
			return res

class _Environment(object):
	""" 
	An environment represents the current execution environment.
	It keeps track of the scoping rules when looking up nodes.
	"""
	def __init__(self):
		super(_Environment, self).__init__()
		self.level = 0
		self.stack = []
		self.stack.append(_Scope())

	def addScope(self):
		self.stack.append(_Scope())
		self.level += 1

	def popScope(self):
		if self.level is not 0:
			self.stack.pop()
			self.level -= 1

	def addEl(self, key, node):
		self.stack[-1].addEl(key, node)

	def getEl(self, key, ctr):
		res = None
		for el in reversed(self.stack):
			res = el.getEl(key)
			if res:
				break
		if res:
			return res
		else:
			err = "Undefined node reference: " + str(key)
			tools.error(err,ctr)

_env = _Environment()

def envGet(key, ctr = "?"):
	return _env.getEl(key, ctr)

def envNode(key, node):
	_env.addEl(int(key), node)

def envNamed(key, node):
	core.runtime.pool.addFunction(key, node)

def envAdd():
	_env.addScope()

def envPop():
	_env.popScope()

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
	envPop()
	envNamed(name, node)
	envAdd()
	envNode(0, node)

def parseSubGraph(arr, ctr):
	pass

def parseGraph(arr, ctr):
	if __PARSING_COMPOUND is 0:
		parseNormalGraph(arr, ctr)
	else:
		parseSubGraph(arr, ctr)

# ----------- #
# Node Parser #
# ----------- #

def parseStandardNode(key, label):
	operation 	= operations.getFunction(key)
	inputs		= operation.func_code.co_argcount
	outputs 	= 1

	node = core.operationnode.OperationNode(inputs, outputs, operation)
	envNode(label, node)

def parseCallNode(label):
	node = core.callnode.CallNode(1,1)
	envNode(label, node)


def parseNode(arr, ctr): 
	key 		= int(arr[_n_code_idx])
	label 		= int(arr[_n_label_idx])

	if key is 120:
		parseCallNode(label)
	else:
		parseStandardNode(key, label)

# --------------- #
# Compound Parser #
# --------------- #

def parseCompoundStart(arr, ctr):
	__PARSING_COMPOUND += 1

def parseCompoundEnd(arr, ctr):
	__PARSING_COMPOUND -= 1
