# type.py
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
# \package if1parser.type
# \brief Type parser
# 
# Discover IF1 types.
# For an introduction on how types are represented in
# IF1, check out the [IF1 reference](md_doc__i_f1.html#types)
#
# \todo Change this to express IF1 types in relation to DVM types
##

import tools

# -------------------- #
# Forward declarations #
# -------------------- #

def _Tag(arr): 		_parseTag(arr) 	
def _Tuple(arr): 	_parseTuple(arr) 
def _Union(arr): 	_parseUnion(arr) 
def _Array(arr): 	_parseArray(arr) 
def _Basic(arr): 	_parseBasic(arr) 
def _Field(arr): 	_parseField(arr) 
def _Record(arr): 	_parseRecord(arr) 
def _Stream(arr): 	_parseStream(arr) 
def _Function(arr): _parseFunction(arr)
def _Multiple(arr): _parseMultiple(arr)

# --------- #
# Constants #
# --------- #

# T <label> <type_code> <arg_1> <arg_2>
_label_idx 	= 1 
_code_idx 	= 2
_arg_1_idx 	= 3
_arg_2_idx 	= 4

## The function that is needed to parse a given idx
_type_codes = {
	 0 : _Array,
	 1 : _Basic,
	 2 : _Field,
	 3 : _Function,
	 4 : _Multiple,
	 5 : _Record,
	 6 : _Stream,
	 7 : _Tag,
	 8 : _Tuple,
	 9 : _Union
}

## Basic type codes and the python types to match them
_basic_types = {
	0 : bool,
	1 : str,  # Python has no built-in charachter
	2 : float,
	3 : int,
	4 : None,
	5 : float,
	6 : str
	#6 : WildBasic 	Type not mentioned in the reference manual
}

# ------------------- #
# Type representation #
# ------------------- #

class _Type(object): pass

##
# Represents any possible type
##
class _UnknownType(_Type):
	def __init__(self):
		super(_UnknownType, self).__init__()
		self.list = []
		self.type = None

	def __str__(self):
		return "Unknown Type"

##
# Represents one of the basic IF1 types.
##
class _BasicType(_Type):
	def __init__(self, type):
		super(_BasicType, self).__init__()
		self.type = type

	def __str__(self):
		return "Basic Type: " + str(self.type)

##
# Wrapper around a container that contains
# a single base type (such as an array)
##
class _ContainerType(_Type):

	def __init__(self, baseType, containerType):
		super(_ContainerType, self).__init__()
		self.base = baseType
		self.container = containerType

	def __str__(self):
		return "Container: " + self.container + " " + self.base.__str__()

##
# Wrapper around a combined type that contains multiple base types
#
# The wrapper represents the full type starting at it's index.
# So if we have a tuple (int, str, int), then we would have 3
# _CombinedType instances, one that represents the full type,
# one that represents (str, int) and one that represents (int).
##
class _CombinedType(_Type):
	def __init__(self, type, containerType, next = None):
		super(_CombinedType, self).__init__()
		self.type = containerType
		self.list = [type]
		if next:
			self.list += next.list

	def __str__(self):
		res = "Combined: (" + self.type + ")"
		for el in self.list:
			res += " <" + str(el) + ">"
		return res

##
# Wrapper around a pointer to the first element of a combined type
##
class _PointerType(_Type):
	def __init__(self, dest, containerType):
		super(_PointerType, self).__init__()
		self.type = containerType
		self.dest = dest

	def __str__(self):
		return "Pointer: (" + self.type + "): " + self.dest

	def follow(self):
		return getType(self.dest)

##
# Wrapper around a function type
##
class _FunctionType(_Type):	
	def __init__(self, args, res):
		super(_FunctionType, self).__init__()
		self.args = args
		self.res = res

	def __str__(self):
		res = "Function: \n"
		res += "\t arg: " + str(self.args) + "\n"
		res += "\t res: " + str(self.res)
		return res

# --------- #
# Type Pool #
# --------- #

##
# Store all the encountered types
##
class _TypePool(object):
	def __init__(self):
		super(_TypePool, self).__init__()
		self._type_pool = {0 : _UnknownType()}

	def __str__(self):
		res = "Type pool:\n"
		for key, value in self._type_pool.iteritems():
			res +=  "\t" + str(key) + ": " +  str(value) + "\n"
		return res

	def addType(self, arr, type):
		key = int(arr[_label_idx])
		self._type_pool.update({key : type})

	def getType(self, key):
		return self._type_pool[int(key)]

_pool = _TypePool()

##
# Get a type from the pool
##
def getType(label):
	return _pool.getType(label)

# ------ #
# Parser #
# ------ #

def parseType(arr, ctr):
	funcKey = int(arr[_code_idx])
	try:
		func = _type_codes[funcKey]
	except KeyError:
		tools.warning("Unknown type code: " + str(funcKey) + " encountered.", ctr)
		_pool.addType(arr, _UnknownType())
	else:
		func(arr)

def _parseBasic(arr):
	base_type = _basic_types[int(arr[_arg_1_idx])]
	_pool.addType(arr, _BasicType(base_type))

def _parseFunction(arr):
	args = getType(arr[_arg_1_idx])
	res  = getType(arr[_arg_2_idx])
	_pool.addType(arr, _FunctionType(args, res))

def _parseContainer(arr, container):
	base_type = getType(arr[_arg_1_idx])
	_pool.addType(arr, _ContainerType(base_type, container))

def _parseCombinedPtr(arr, container):
	dest = arr[_arg_1_idx]
	_pool.addType(arr, _PointerType(container, dest))

def _parseCombined(arr, container):
	baseType = getType(arr[_arg_1_idx])
	
	# Add the new type, if there is a previous, link to it
	try:
		next = getType(arr[_arg_2_idx])
	except KeyError:
		_pool.addType(arr, _CombinedType(baseType, container))
	else:
		_pool.addType(arr, _CombinedType(baseType, container, next))

def _parseTag(arr): 		_parseCombined(arr, "tag")
def _parseTuple(arr): 		_parseCombined(arr, "tuple")
def _parseField(arr): 		_parseCombined(arr, "field") 
def _parseArray(arr):		_parseContainer(arr, "array")
def _parseStream(arr):		_parseContainer(arr, "stream")
def _parseMultiple(arr):	_parseContainer(arr, "multiple")
def _parseUnion(arr):		_parseCombinedPtr(arr, "Union") 
def _parseRecord(arr): 		_parseCombinedPtr(arr, "Record")