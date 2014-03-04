# operations.py
# Mathijs Saey
# DVM

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
# \package natives
# \brief DVM Native Operations
# 
# This module defines all of the native DVM
# operations.
##

import math
import copy

# ------------- #
# Type Creation #
# ------------- #

## Return the DVM void type.
def dvm_Void(): return None
## Create a DVM Boolean
def dvm_Bool(x): return bool(x)
## Create a DVM Integer
def dvm_Int(x): return int(x)
## Create a DVM Float
def dvm_Float(x): return float(x)
## create a DVM String
def dvm_String(x): return str(x)

## 
# Create a DVM Array
# 
# DVM arrays are indexed starting from 0.
##
def dvm_Array(*x): return list(x)

# ----------------- #
# General Operators #
# ----------------- #

##
# Do nothing.
#
# \param x Any number of inputs
# \return Nothing.
##
def dvm_noOp(*x): pass

##
# See if the element is void.
# \param x A parameter of any type.
# \return True if x is void.
##
def dvm_isVoid(x): return x == None

##
# Check if 2 elements are equal.
#
# \param l, r parameters of any type. 
# \return True if l and r are equal.
##
def dvm_equals(l, r): return l == r

##
# Check if 2 elements are not equal.
#
# \param l, r parameters of any type. 
# \return True if l and r are **not** equal
##
def dvm_notEqual(l, r): return l != r

# ----------------- #
# Boolean Operators #
# ----------------- #

## 
# Logical and
#
# param l, r booleans
# \return A boolean
##
def dvm_and(l, r): return l and r

## 
# Logical Or
#
# param l, r booleans
# \return A boolean
##
def dvm_or(l, r): return l or r

##
# Logical xor
#
# param l, r booleans
# \return a boolean
##
def dvm_xor(l, r): return l ^ r

##
# Negation
#
# \param x a boolean
# \return the negate boolean
##
def dvm_not(x): return not x

# ----------------- #
# Numeric Operators #
# ----------------- #

## 
# Negation
#
# \param x a number
# \return negated x
##
def dvm_neg(x): return - x

##
# Addition.
#
# param l, r numeric parameters
# \return A number
##
def dvm_add(l, r): return l + r

##
# Subtraction.
#
# param l, r numeric parameters
# \return A number
##
def dvm_sub(l, r): return l - r

##
# Multiplication.
#
# param l, r numeric parameters
# \return A number
##
def dvm_mul(l, r): return l * r

##
# Subtraction.
#
# param l, r numeric parameters
# \return A number
##
def dvm_div(l, r): return l / (r * 1.0)

##
# Round down
#
# \param x A number
# \return A number
##
def dvm_floor(x): return math.floor(x)

##
# Round up
#
# \param x A number
# \return A number
##
def dvm_ceil(x): return math.ceil(x)

## 
# Maximum
#
# param l, r numeric parameters
# \return A number
##
def dvm_min(l, r): return min(l, r)

## 
# Minimum
#
# param l, r numeric parameters
# \return A number
##
def dvm_max(l, r): return max(l, r)

# ------------------ #
# Numeric Comparison #
# ------------------ #

##
# Smaller than
#
# param l, r numbers
# \return true if l < r
##
def dvm_less(l, r): return l < r

##
# Greater than
#
# param l, r numbers
# \return true if l > r
##
def dvm_more(l, r): return l > r

##
# Smaller or equal than
#
# param l, r numbers
# \return true if l =< r
##
def dvm_less_eq(l, r): return l <= r

##
# Greatar or equal than
#
# param l, r numbers
# \return true if l >= r
##
def dvm_more_eq(l, r): return l >= r

# ----------------- #
# String Operations #
# ----------------- #

##
# See if a string contains a value.
#
# param str, x strings
# \return True if x is an element of str
##
def dvm_str_contains(str, x): return x in str

##
# Return the idx of x in str.
#
# param str, x strings
# \return 
#	the idx of x in str.
#	-1 if x is not in str.
##
def dvm_str_find(str, x): return str.find(x)

##
# Conver a string to upper case.
#
# \param str a string
# \return the string in upper case.
##
def dvm_str_upper(str): return str.upper()

##
# Conver a string to lower case.
#
# \param str a string
# \return the string in lower case.
##
def dvm_str_lower(str): return str.lower()

##
# Get a substring.
#
# \param str a string
# \param start the index to start at.
# \param stop the index to stop at.
##
def dvm_str_sub(str, start, stop): return str[start:stop]

##
# Reverse a string.
#
# \param str a string
# \return the reversed string
##
def dvm_str_reverse(str): return str[::-1]

##
# Append 2 strings.
# 
# \param l, r strings
# \return the combination of 2 strings.
##
def dvm_str_append(l, r): return l + r

# ---------------- #
# Array Operations #
# ---------------- #

##
# See if an array is empty.
#
# \param arr the array
# \return True if the array is empty
##
def dvm_arr_isEmpty(arr): return arr == []

##
# Get the length of an array.
#
# \param arr An array
# \return the length of the array.
##
def dvm_arr_length(arr): return len(arr)

##
# Create an empty array
##
def dvm_arr_empty(): return []

##
# Create an array filled with an element
#
# \param length the length of the array
# \param fill the element to fill the array with
# \return the new array
##
def dvm_arr_create(length, fill): return [fill] * length

##
# Get an element from the array.
#
# \param arr the array to taken an element from
# \param idx the indes to access
# \return the element arr[idx]
##
def dvm_arr_get(arr, idx): return arr[idx]

##
# Create a new array with a different
# element at idx.
#
# \param arr the array
# \param idx the index to modify
# \param el the element to insert
# \return 
#	a new array that is identical to
#	arr, with the element at idx replaced by el
##
def dvm_arr_set(arr, idx, el):
	res = copy.deepcopy(arr)
	res[idx] = el
	return res

##
# Insert elements into an array.
#
# e.g: 
#    
#     test = [1,2,3]
#     >>> natives.dvm_arr_insert(test, 1, 'a', 'b')
#     [1, 'a', 'b', 2, 3]
#
# \param arr the array
# \param idx the start index
# \param el the elements to include.
# \return 
#	A new array, which consists of arr
#	with the elements added at index.
#	The elements are inserted at index, but 
#	do not replace anything after index.
##
def dvm_arr_insert(arr, idx, *el): 
	res = copy.deepcopy(arr)
	pre = res[:idx]
	pos = res[idx:]
	return pre + list(el) + pos

##
# Replace elements in an array. 
# Similar to dvm_arr_insert, but
# replaces the elemets starting at idx.
#
# e.g: 
#    
#     test = [1,2,3]
#     >>> natives.dvm_arr_replace(test, 1, 'a', 'b')
#     [1, 'a', 'b']
#
# \param arr the array
# \param idx the start index
# \param el the elements to include.
# \return 
#		A new array, with the elements
#		starting at idx replaced by el.
##
def dvm_arr_replace(arr, idx, *el):
	res = copy.deepcopy(arr)
	res[idx:len(el) + 1] = el
	return res

##
# Array concatenation.
#
# \param l,r arrays.
# \return concatenation of l and r.
##
def dvm_arr_catenate(l, r):
	return l + r

##
# Add an element to the start of an array.
#
# \param arr An array
# \param el The element to add.
# \return 
#		a copy of arr with el 
#		added in front.
##
def dvm_arr_add_front(arr, el):
	return [el] + arr

##
# Add an element to the back of an array.
#
# \param arr An array
# \param el The element to add.
# \return 
#		a copy of arr with el 
#		added to the back.
##
def dvm_arr_add_back(arr, el):
	return arr + [el]

##
# Get a subset of an array
#
# \param arr An array
# \param start The idx to start at.
# \param stop The idx to stop at.
# \return 
#		An array containing the elements of 
#		arr between start and stop.
##
def dvm_arr_sub(arr, start, stop):
	return arr[start:stop]

## 
# Contains references to all
# the operations.
##
operations = { 
	'void'        : dvm_Void,
	'bool'        : dvm_Bool,
	'int'         : dvm_Int,
	'float'       : dvm_Float,
	'string'      : dvm_String,
	'array'       : dvm_Array,

	'noOp'        : dvm_noOp,
	'isVoid'      : dvm_isVoid,
	'equals'      : dvm_equals,
	'notEq'       : dvm_notEqual,

	'and'         : dvm_and,
	'or'          : dvm_or,
	'xor'         : dvm_xor,
	'not'         : dvm_not,

	'neg'         : dvm_neg,
	'add'         : dvm_add,
	'sub'         : dvm_sub,
	'mul'         : dvm_mul,
	'div'         : dvm_div,
	'floor'       : dvm_floor,
	'ceil'        : dvm_ceil,
	'min'         : dvm_min,
	'max'         : dvm_max,
	'less'        : dvm_less,
	'more'        : dvm_more,
	'lessEq'      : dvm_less_eq,
	'moreEq'      : dvm_more_eq,

	'strContains' : dvm_str_contains,
	'strFind'     : dvm_str_find,
	'strUpper'    : dvm_str_upper,
	'strLower'    : dvm_str_lower,
	'strSub'      : dvm_str_sub,
	'strRev'      : dvm_str_reverse,
	'strApp'      : dvm_str_append,

	'arrEmpty'    : dvm_arr_isEmpty,
	'arrLen'      : dvm_arr_length,
	'arrEmpty'    : dvm_arr_empty,
	'arrCreate'   : dvm_arr_create,
	'arrGet'      : dvm_arr_get,
	'arrSet'      : dvm_arr_set,
	'arrIns'      : dvm_arr_insert,
	'arrRepl'     : dvm_arr_replace,
	'arrCat'      : dvm_arr_catenate,
	'arrFrnt'     : dvm_arr_add_front,
	'arrBck'      : dvm_arr_add_back,
	'arrSub'      : dvm_arr_sub 
}
