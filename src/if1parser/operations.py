# operations.py
# Mathijs Saey
# dvm prototype

"""
This module allows us to retrieve python versions of the base
IF1 nodes.

"""

# ---------------- #
# Public functions #
# ---------------- #

# Get a function by it's IF1 label.
def getFunction(label): pass

# -------------------- #
# Function Definitions #
# -------------------- #

def NoOp(*args): pass

def AAddH(arr, el): 
	return arr += [el]

def AAddL(arr, el):
	return [el] += arr

def ABuild(bound, *elements):
	return list(elements)

def ACatenate(arr, *arrs):
	res = arr
	for el in arrs:
		res += el
	return res

def AElement(arr, idx):
	return arr[idx]

# ---------------- #
# Function Mapping #
# ---------------- #

from functools import partial

def unkownFunction(name, *args):
	print "Undefined IF1 function with name:", name, "encountered."

_functions = {
	100 : AAddH,
	101 : AAddL,
	102 : partial(unkownFunction, "AAdjust")
	103 : ABuild,
	104 : ACatenate,
	105 : AElement,
	106 : AFill,
	107 : AGather,
	108 : AIsEmpty,
	109 : ALimH,
	110 : ALimL,
	111 : ARemH,
	112 : ARemL,
	113 : AReplace,
	114 : AScatter,
	115 : ASetL,
	116 : ASize,
	117 : Abs,
	118 : BindArguments,
	119 : Bool,
	120 : Call,
	121 : Char,
	122 : Div,
	123 : Double,
	124 : Equal,
	125 : Exp,
	126 : FirstValue,
	127 : FinalValue,
	128 : Floor,
	129 : Int,
	130 : IsError,
	131 : Less,
	132 : LessEqual,
	133 : Max,
	134 : Min,
	135 : Minus,
	136 : Mod,
	137 : Neg,
	138 : NoOp,
	139 : Not,
	140 : NotEqual,
	141 : Plus,
	142 : RangeGenerate,
	143 : RBuild,
	144 : RElements,
	145 : RReplace,
	146 : RedLeft,
	147 : RedRight,
	148 : RedTree,
	149 : Reduce,
	150 : RestValues,
	151 : Single,
	152 : Times,
	153 : Trunc,
	154 : PrefixSize,
	155 : Error,
	156 : ReplaceMulti,
	157 : Convert,
	158 : CallForeign,
	159 : AElementN,
	160 : AElementP,
	161 : AElementM,
	170 : AAddLAT,
	171 : AAddHAT,
	172 : ABufPartition,
	173 : ABuildAT,
	174 : ABufScatter,
	175 : ACatenateAT,
	176 : AElementAT,
	177 : AExtractAT,
	178 : AFillAT,
	179 : AGatherAT,
	180 : ARemHAT,
	181 : ARemLAT,
	182 : AReplaceAT,
	183 : ArrayToBuf,
	184 : ASetLAT,
	185 : DefArrayBuf,
	186 : DefRecordBuf,
	187 : FinalValueAT,
	188 : MemAlloc,
	189 : BufElements,
	190 : RBuildAT,
	191 : RecordToBuf,
	192 : RElementsAT,
	193 : ReduceAT,
	19  : ShiftBuffer,
	195 : ScatterBufPartitions,
	196 : RedLeftAT,
	197 : RedRightAT,
	198 : RedTreeAT
}

def getFunction(label):
	key = int(label)
	try:
		func = _functions[key]
	except KeyError:
		print "Cannot find function with label:", label, "NoOp will be used instead."
		return NoOp
	else: 
		return func
