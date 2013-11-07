# operations.py
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
This module allows us to retrieve python versions of the base
IF1 nodes.

"""

from functools 	import partial
from math 		import floor

import core.compoundnode

import tools
import graph

# ---------------- #
# Public functions #
# ---------------- #

def getFunction(label): pass
def getCompound(label): pass

# -------------- #
# Compound Nodes #
# -------------- #

def unknownCompound(*args):
	err = "Undefined compound node encountered."
	tools.error(err)

_compound = {
	0 	: 	unknownCompound,
	1 	: 	core.compoundnode.SelectNode,
	2 	: 	unknownCompound,
	3 	: 	unknownCompound,
	4 	: 	unknownCompound,
	5 	: 	unknownCompound,
	6 	: 	unknownCompound,
	7 	: 	unknownCompound,
	8 	: 	unknownCompound,
	9 	: 	unknownCompound,
	10	: 	unknownCompound
}

def getCompound(label, ctr = "?"):
	key = int(label)
	try:
		node = _compound[key]
	except KeyError:
		tools.err("Unkown compound node, " + label + " requested.", ctr)
	else: 
		return node

# -------------------- #
# Function Definitions #
# -------------------- #

def NoOp(*args): 					pass
def ALimL(arr): 					return 0
def Not(x):							return not x
def Mod(l,r):						return l % r
def Minus(l,r):						return l - r
def Exp(l, r): 						return l ** r
def Max(l,r): 						return max(l,r)
def Min(l,r):						return min(l,r)
def ASize(arr): 					return len(arr)
def Less(l,r): 						return l < r
def Div(l, r): 						return l / r
def Equal(l, r): 					return l == r
def NotEqual(l, r): 				return l != r
def LessEqual(l,r):					return l <= r
def Neg(arith):						return - arith
def ARemL(arr): 					return arr[1:]
def ALimH(arr): 					return len(arr)
def Bool(int): 						return bool(int)
def Abs(arith): 					return abs(arith)
def Floor(int): 					return floor(int)
def Double(int): 					return int + 0.0
def AIsEmpty(arr): 					return arr == []
def RangeGenerate(l, h): 			return range(l,h)
def Single(val): 					return float(val)
def Char(int): 						return str(unichr(int))
def AAddL(arr, el): 				return [el] + arr
def AElement(arr, idx): 			return arr[idx]
def ARemH(arr): 					return arr[:len(arr) - 1]
def AAddH(arr, el): 				return arr[:] + [el]
def ABuild(bound, *elements): 		return list(elements)
def BindArguments(func, *args): 	return partial(func, args)

def RedLeft(func, acc, mult, filt): 
	print "TODO: see if foldl is still needed with compound nodes"
def RedRight(func, acc, mult, filt): 
	print "TODO: see if foldl is still needed with compound nodes"
def RedTree(func, acc, mult, filt): 
	print "TODO: see if foldl is still needed with compound nodes"
def Reduce(func, acc, mult, filt): 
	print "TODO: see if foldl is still needed with compound nodes"

def ASetL(arr, idx): 				
	print "ASetL not supported in IF1 subset..."
def AScatter(arr): 					
	print "TODO: see if ASCatter is still needed with compound nodes"


def ACatenate(arr, *arrs):
	res = arr[:]
	for el in arrs:
		res += el
	return res

def AFill(l, h, *el):
	if h > l:
		return list(el) * (h - l)
	else: 
		return []

def AGather(l, arr, filter = None):
	res = []
	filt = filter
	if filt is None:
		filt = [True] * len(arr)

	for idx in xrange(0,len(arr)):
		el = arr[idx]
		b = filt[idx]
		if b:
			res += el
	return res

def AReplace(arr, idx, *args):
	end = idx + len(args)
	res = arr[:]
	res[idx:end] = args
	return res

def FirstValue(mult, filter = None):
	filt = filter
	if filt is None:
		filt = [True] * len(mult)

	for idx in xrange(0,len(mult)):
		if filt[idx]:
			return mult[idx]

def FinalValue(mult, filter = None):
	filt = filter
	mult.reverse()
	if filt is None:
		filt = [True] * len(mult)

	for idx in xrange(0,len(mult)):
		if filt[idx]:
			return mult[idx]

def Int(x):
	if isinstance(x, float):
		x += 0.5
	return int(x)

def Plus(l,r):
	if isinstance(l, bool):
		return l or r
	else:
		return l + r

def Times(l,r):
	if isinstance(l, bool):
		return l and r
	else:
		return l * r

# ---------------- #
# Function Mapping #
# ---------------- #

def unkownFunctionError(name, *args):
	err = "Undefined IF1 function with name: " + name + " encountered."
	tools.error(err)

def createPartial(name):
	return partial(unkownFunctionError, name)

_functions = {
	100 : AAddH,
	101 : AAddL,
	102 : createPartial("AAdjust"),
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
	#120 : Call,
	121 : Char,
	122 : Div,
	123 : Double,
	124 : Equal,
	125 : Exp,
	126 : FirstValue,
	127 : FinalValue,
	128 : Floor,
	129 : Int,
	130 : createPartial("IsError"),
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
	143 : createPartial("RBuild"),
	144 : createPartial("RElements"),
	145 : createPartial("RReplace"),
	146 : createPartial("RedLeft"),
	147 : createPartial("RedRight"),
	148 : createPartial("RedTree"),
	149 : createPartial("Reduce"),
	150 : createPartial("RestValues"),
	151 : Single,
	152 : Times,
	153 : createPartial("Trunc"),
	154 : createPartial("PrefixSize"),
	155 : createPartial("Error"),
	156 : createPartial("ReplaceMulti"),
	157 : createPartial("Convert"),
	158 : createPartial("CallForeign"),
	159 : createPartial("AElementN"),
	160 : createPartial("AElementP"),
	161 : createPartial("AElementM"),
	170 : createPartial("AAddLAT"),
	171 : createPartial("AAddHAT"),
	172 : createPartial("ABufPartition"),
	173 : createPartial("ABuildAT"),
	174 : createPartial("ABufScatter"),
	175 : createPartial("ACatenateAT"),
	176 : createPartial("AElementAT"),
	177 : createPartial("AExtractAT"),
	178 : createPartial("AFillAT"),
	179 : createPartial("AGatherAT"),
	180 : createPartial("ARemHAT"),
	181 : createPartial("ARemLAT"),
	182 : createPartial("AReplaceAT"),
	183 : createPartial("ArrayToBuf"),
	184 : createPartial("ASetLAT"),
	185 : createPartial("DefArrayBuf"),
	186 : createPartial("DefRecordBuf"),
	187 : createPartial("FinalValueAT"),
	188 : createPartial("MemAlloc"),
	189 : createPartial("BufElements"),
	190 : createPartial("RBuildAT"),
	191 : createPartial("RecordToBuf"),
	192 : createPartial("RElementsAT"),
	193 : createPartial("ReduceAT"),
	19  : createPartial("ShiftBuffer"),
	195 : createPartial("ScatterBufPartitions"),
	196 : createPartial("RedLeftAT"),
	197 : createPartial("RedRightAT"),
	198 : createPartial("RedTreeAT")
}

def getFunction(label, ctr = "?"):
	key = int(label)
	try:
		func = _functions[key]
	except KeyError:
		tools.warning("Cannot find function with label: " + label + " NoOp will be used instead.", ctr)
		return NoOp
	else: 
		return func
