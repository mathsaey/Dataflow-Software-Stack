# types.py
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
# \package native.types
# \brief DVM native types
# 
# This module defines the native types
# that DVM defines.
#
# In general, DVM types map to the underlying python types.
# The functions in this module serve a dual purpose.
# Firstly, they serve as type casts to create the underlying 
# DVM type. Secondly, they serve as documentation for the various
# types that dvm offers.
##

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