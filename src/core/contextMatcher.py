# contextMatcher.py
# Mathijs Saey
# dvm prototype

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
Context matcher.

The context matcher is responsible for gathering tokens
with the same context before sending them to the instruction they belong to.

The following functions can be used by other modules

addToken(token)           
	Add a token to the context matcher

initLitArr(inst, inputs)  
	Create a literal container for an instruction.
		inst is the key of the instruction
		inputs is the amount of inputs the instruction accepts
"""

import copy
import runtime

# ------- #
# Storage #
# ------- #

__LITERALS__ = {}
__TOKENS__ = {}

# -------- #
# Literals #
# -------- #

# Create a literal array for instructions
# Should be called when creating an instruction
def initLitArr(inst, inputs):
	arr = [None] * inputs
	__LITERALS__.update({inst : arr})

# Add a permanent literal to an instruction
def _addLiteral(inst, port, token):
	arr = __LITERALS__[inst]
	arr[port] = token

# --------------- #
# Standard Tokens #
# --------------- #

# See if we already have a token array for a given key
# if not, create one
def _checkKey(key):
	if key not in __TOKENS__:
		arr = copy.copy(__LITERALS__[key[0]])
		__TOKENS__.update({key:arr})

# Add a token to an array
def _updateKeyArr(key, port, token):
	arr = __TOKENS__[key]
	arr[port] = token

# See if a certain array is ready
def _isKeyReady(key):
	return __TOKENS__[key].count(None) == 0

# Execute an instruction with inputs
# from a given context
def _executeKey(key):
	arr = __TOKENS__[key]
	del __TOKENS__[key]	
	runtime.addInstruction(key[0], arr)

# Add a token to the matcher
def addToken(token):
	tag  = token.tag                  
	inst = tag.inst                   
	cont = tag.cont                   
	port = tag.port                   
	key  = (inst, cont)               

	if tag.isLiteral():               
		_addLiteral(inst, port, token) 

	_checkKey(key)                     
	_updateKeyArr(key, port, token)    
	if _isKeyReady(key):               
		_executeKey(key)
