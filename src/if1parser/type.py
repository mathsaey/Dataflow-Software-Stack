# type.py
# Mathijs Saey
# dvm prototype

# T <label> <type_code> <arg_1> <arg_2>
_label_idx 	= 1
_code_idx 	= 2
_arg_1_idx 	= 3
_arg_2_idx 	= 4

type_pool = {}

def update_pool(arr, type):
	type_pool.update({int(arr[_label_idx]) : type})
def update_pool_idx(key, type):
	type_pool.update({key : type})

def get_pool(label):
	return type_pool[int(label)]

# Basic type codes and the python types to match them
basic_types = {
	0 : bool,
	1 : str,  # Python has no built-in charachter
	2 : float,
	3 : int,
	4 : None,
	5 : float,
	6 : str
	#6 : WildBasic 	Type not mentioned in the reference manual
}

def Basic(arr):
	base_type = basic_types[int(arr[_arg_1_idx])]
	update_pool(arr, base_type)

def Array(arr):
	base_type = get_pool(arr[_arg_1_idx])
	update_pool(arr, [base_type])

tuples = {}

def Tuple(arr):
	# Get the label
	label = arr[_label_idx]
	rootKey = 0

	if label not in tuples:
		tuples.update({label : []})
		rootKey = label
	else: 
		rootKey = tuples[label]

	# Get the current tuple status
	rootLst = tuples[rootKey]
	# Add the current element to the list
	rootLst = rootLst + [get_pool(arr[_arg_1_idx])]
	tuples[rootKey] = rootLst

	if int(arr[_arg_2_idx]) == 0:
		# If the tuple is complete, add it to the pool
		update_pool_idx(rootKey, tuple(rootLst))
		del tuples[rootKey]
	else: 
		# Get the next element idx and store the 
		# idx of the root element
		next = arr[_arg_2_idx]
		tuples.update({next : rootKey})
		del tuples[label]
	

def Field(arr):
	pass
def Function(arr):
	pass
def Multiple(arr):
	pass
def Record(arr):
	pass
def Stream(arr):
	pass
def Tag(arr):
	pass
def Union(arr):
	pass
def Unknown(arr):
	pass

# Type codes and the functions to parse them
type_codes = {
	0 : Array,
	1 : Basic,
	2 : Field,
	3 : Function,
	4 : Multiple,
	5 : Record,
	6 : Stream,
	7 : Tag,
	8 : Tuple,
	9 : Union,
	10 : Unknown
}

def parse_type(arr):
	funcKey = int(arr[_code_idx])
	type_codes[funcKey](arr)
