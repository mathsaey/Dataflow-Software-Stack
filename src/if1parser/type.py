# type.py
# Mathijs Saey
# dvm prototype
		
""" 
IF1 type parser

This module defines the functions that allow
us to parse type declarations and to retrieve
the type that corresponds to a certain label.

Types are stored as the closest matching python type.

"""
# ---------------- #
# Public functions #
# ---------------- #

def parseType(arr): pass
def getType(label): pass

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

# The function that is needed to parse a given idx
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

# Basic type codes and the python types to match them
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

class _BasicType(_Type):
	""" Wrapper around a basic type """

	def __init__(self, type):
		super(_BasicType, self).__init__()
		self.type = type

	def __str__(self):
		if self.type:
			res = "Basic Type: " + self.type.__name__
		else:
			res = "None"
		return res

class _ContainerType(_Type):
	""" Wrapper around a container that contains a single base type """

	def __init__(self, baseType, containerType):
		super(_ContainerType, self).__init__()
		self.base = baseType
		self.container = containerType

	def __str__(self):
		res = "Container: " + self.container + " " + self.base.__str__()
		return res

class _CombinedType(_Type):
	""" Wrapper around a combined type that contains multiple base types

	The wrapper represents the full type starting at it's index.
	So if we have a tuple (int, str, int), then we would have 3
	_CombinedType instances, one that represents the full type,
	one that represents (str, int) and one that represents (int).
	"""

	def __init__(self, type, containerType, next = None):
		super(_CombinedType, self).__init__()
		self.type = containerType
		self.list = [type]
		if next:
			self.list += next.list

	def __str__(self):
		res = "Combined: (" + self.type + ")"
		for el in self.list:
			res += " <" + el.__str__() + ">"
		return res

class _PointerType(_Type):
	""" Wrapper around a pointer to the first element of a combined type """

	def __init__(self, dest, containerType):
		super(_PointerType, self).__init__()
		self.type = containerType
		self.dest = dest

	def __str__(self):
		return "Pointer: (" + self.type + "): " + self.dest

	def follow(self):
		return getType(self.dest)

class _FunctionType(_Type):
	""" Wrapper around a function type """
	
	def __init__(self, args, res):
		super(_FunctionType, self).__init__()
		self.args = args
		self.res = res

	def __str__(self):
		res = "Function: \n"
		res += "\t arg: " + self.args.__str__() + "\n"
		res += "\t res: " + self.res.__str__()
		return res

# --------- #
# Type Pool #
# --------- #

class _TypePool(object):
	"""A type pool object stores all the encountered types"""

	def __init__(self):
		super(_TypePool, self).__init__()
		self._type_pool = {}

	def __str__(self):
		res = "Type pool:\n"
		for key, value in self._type_pool.iteritems():
			res +=  "\t" + key.__str__() + ": " +  value.__str__() + "\n"
		return res

	def addType(self, arr, type):
		key = int(arr[_label_idx])
		self._type_pool.update({key : type})

	def getType(self, key):
		return self._type_pool[int(key)]

_pool = _TypePool()

def getType(label):
	return _pool.getType(label)

# ------ #
# Parser #
# ------ #

def parseType(arr):
	funcKey = int(arr[_code_idx])
	try:
		_type_codes[funcKey](arr)
	except KeyError:
		print "Unknown type code:", funcKey, "encountered"

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
	label = arr[_label_idx]
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