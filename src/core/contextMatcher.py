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
This module defines the context matcher.

The context matcher is responsible for gathering tokens
with the same context before sending them to the instruction they belong to.
"""

import copy
import runtime

# ---------------- #
# Public functions #
# ---------------- #

# Add a token to the matcher
def addToken(token):
	tag  = token.tag                     # The Tag of the token
	inst = tag.inst                      # The key of the instruction
	cont = tag.cont                      # The context of the token
	port = tag.port                      # The slote where we enter our token
	key  = (inst, cont)                  # The (inst, context) pair

	if tag.isLiteral():                  # Add Literals if needed
		addLiteral(inst, port, token)    # We also add the literals to the normal token

	checkKey(key)                        # Create array if it's not there
	updateKeyArr(key, port, token)       # Add the token to the port
	if isKeyReady(key):                  # Execute if we have all the inputs
		executeKey(key)

# Create a literal array for instructions
# Should be called when creating an instruction
def initLitArr(inst, inputs):
	arr = [None] * inputs
	__LITERALS__.update({inst : arr})

# ---------------- #
# Helper functions #
# ---------------- #

__LITERALS__ = {}
__TOKENS__ = {}


# Add a permanent literal to an instruction
def addLiteral(inst, port, token):
	arr = __LITERALS__[inst]
	arr[port] = token

# See if we already have a token array for a given key
# if not, create one
def checkKey(key):
	if key not in __TOKENS__:
		arr = copy.copy(__LITERALS__[key[0]])
		__TOKENS__.update({key:arr})

# Add a token to an array
def updateKeyArr(key, port, token):
	arr = __LITERALS__[key]
	arr[port] = token

# See if a certain array is ready
def isKeyReady(key):
	return __TOKENS__[key].count(None) == 0

# Execute an instruction with inputs
# from a given context
def executeKey(key):
	arr = __TOKENS__[key]
	del __TOKENS__[key]	

	inputs = map(lambda x : x.datum, arr)
	runtime.addInstruction(key[0], inputs)
