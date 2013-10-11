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
def _Unknown(arr): 	_parseUnknown(arr) 
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
	 9 : _Union,
	10 : _Unknown
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

#############
# Type Pool #
#############

class _TypePool(object):
	"""A type pool object stores all the encountered types"""

	def __init__(self):
		super(_TypePool, self).__init__()
		self._type_pool = {}

	def addType(self, arr, type):
		key = int(arr[_label_idx])
		self._type_pool.update({key : type})
	def addTypeIdx(self, key, type):
		self._type_pool.update({key : type})

	def getType(self, key):
		return self._type_pool[int(key)]

_pool = _TypePool()

def getType(label):
	_pool.getType(label)

##########
# Parser #
##########

def parseType(arr):
	funcKey = int(arr[_code_idx])
	_type_codes[funcKey](arr)

# Placeholders

def _parseTag(arr): 		pass 	
def _parseTuple(arr): 		pass 
def _parseUnion(arr): 		pass 
def _parseArray(arr): 		pass 
def _parseBasic(arr): 		pass 
def _parseField(arr): 		pass 
def _parseRecord(arr): 		pass 
def _parseStream(arr): 		pass 
def _parseUnknown(arr): 	pass 
def _parseFunction(arr): 	pass
def _parseMultiple(arr): 	pass


def _parseBasic(arr):
	base_type = _basic_types[int(arr[_arg_1_idx])]
	_pool.addType(arr, base_type)

def _parseArray(arr):
	base_type = _pool.getType(arr[_arg_1_idx])
	_pool.addType(arr, [base_type])