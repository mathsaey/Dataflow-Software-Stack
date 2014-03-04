# operations.py
# Mathijs Saey
# IDIS

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

"""
IF1 node functions

This module defines python equivalents of the if1 native nodes.

When requesting the function for a given key, this module will return a
(function, inputs, outputs) tuple.

functions can be requested with the getFunction function.
"""

import math
import tools
import functools

# -------------------- #
# Function Definitions #
# -------------------- #

def NoOp(*args):                return args
def ALimL(arr):                 return 0
def Not(x):                     return not x
def Mod(l,r):                   return l % r
def Minus(l,r):                 return l - r
def Exp(l, r):                  return l ** r
def Max(l,r):                   return max(l,r)
def Min(l,r):                   return min(l,r)
def ASize(arr):                 return len(arr)
def Less(l,r):                  return l < r
def Div(l, r):                  return l / r
def Equal(l, r):                return l == r
def NotEqual(l, r):             return l != r
def LessEqual(l,r):             return l <= r
def Neg(arith):                 return - arith
def ARemL(arr):                 return arr[1:]
def ALimH(arr):                 return len(arr)
def Bool(int):                  return bool(int)
def Abs(arith):                 return abs(arith)
def Floor(int):                 return math.floor(int)
def Double(int):                return int + 0.0
def AIsEmpty(arr):              return arr == []
def RangeGenerate(l, h):        return range(l,h)
def Single(val):                return float(val)
def Char(int):                  return str(unichr(int))
def AAddL(arr, el):             return [el] + arr
def AElement(arr, idx):         return arr[idx]
def ARemH(arr):                 return arr[:len(arr) - 1]
def AAddH(arr, el):             return arr[:] + [el]
def ABuild(bound, *elements):   return list(elements)
def BindArguments(func, *args): return functools.partial(func, args)

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

_functions = {
	100 : AAddH,
	101 : AAddL,
#	102 : AAdjust,
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
#	120 : Call,
	121 : Char,
	122 : Div,
	123 : Double,
	124 : Equal,
	125 : Exp,
	126 : FirstValue,
	127 : FinalValue,
	128 : Floor,
	129 : Int,
#	130 : IsError,
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
#	143 : RBuild,
#	144 : RElements,
#	145 : RReplace,
#	146 : RedLeft,
#	147 : RedRight,
#	148 : RedTree,
#	149 : Reduce,
#	150 : RestValues,
	151 : Single,
	152 : Times,
#	153 : Trunc,
#	154 : PrefixSize,
#	155 : Error,
#	156 : ReplaceMulti,
#	157 : Convert,
#	158 : CallForeign,
#	159 : AElementN,
#	160 : AElementP,
#	161 : AElementM,
#	170 : AAddLAT,
#	171 : AAddHAT,
#	172 : ABufPartition,
#	173 : ABuildAT,
#	174 : ABufScatter,
#	175 : ACatenateAT,
#	176 : AElementAT,
#	177 : AExtractAT,
#	178 : AFillAT,
#	179 : AGatherAT,
#	180 : ARemHAT,
#	181 : ARemLAT,
#	182 : AReplaceAT,
#	183 : ArrayToBuf,
#	184 : ASetLAT,
#	185 : DefArrayBuf,
#	186 : DefRecordBuf,
#	187 : FinalValueAT,
#	188 : MemAlloc,
#	189 : BufElements,
#	190 : RBuildAT,
#	191 : RecordToBuf,
#	192 : RElementsAT,
#	193 : ReduceAT,
#	19  : ShiftBuffer,
#	195 : ScatterBufPartitions,
#	196 : RedLeftAT,
#	197 : RedRightAT,
#	198 : RedTreeAT
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
