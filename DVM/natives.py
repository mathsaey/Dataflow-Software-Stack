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
# \package native.operations
# \brief DVM Native Operations
# 
# This module defines all of the native operations
# that DVM defines.
##

# ------------- #
# Type Creation #
# ------------- #

## Return the DVM void type.
def dvmVoid(): return None
## Create a DVM Boolean
def dvmBool(x): return bool(x)
## Create a DVM Integer
def dvmInt(x): return int(x)
## Create a DVM Float
def dvmFloat(x): return float(x)
## create a DVM String
def dvmString(x): return str(x)
## Create a DVM Array
def dvmArray(*x): return list(x)

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
# \return True if x is none.
##
def dvm_isVoid(x): return x == None

##
# Check if 2 elements are equal.
# \param l a parameter of any type. 
# \param r a parameter of any type.
# \return True if l and r are empty.
#
def dvm_equals(l,r): return l == r

# ----------------- #
# Boolean Operators #
# ----------------- #

## 
# Logical and
#
# \param l A boolean
# \param r A boolean
# \return A boolean
##
def dvm_and(l, r): return l and r
## 
# Logical Or
#
# \param l A boolean
# \param r A boolean
# \return A boolean
##
def dvm_or(l,r): return l or r

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
# Addition.
#
# \param l A numeric parameter
# \param r A numeric parameter
# \return A number
##
def dvm_add(l, r): return l + r

## 
# Contains references to all
# the operations.
##
operations = [
	dvm_noOp, # 0
	dvm_add   # 1
]

