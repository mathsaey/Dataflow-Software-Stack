# main.py
# Mathijs Saey
# dvm

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
This module serves as a top level file to access the other modules
"""

# import if1parser
# import compiler.dot

# #loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/sort.if1"
# loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/select.if1"
# #loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/call.if1"

# def tmp(node):
# 	print node

# if1parser.parseFile(loc)
# compiler.dot.runDot(path="../igr.dot", skipCompound = True)

## TEST CODE ##

import dvm 
import dvm.token
import dvm.runtime

def tOP(a,b):
	return a + b

# # function
fStart = dvm.addSink()
body = dvm.addOperationInstruction(tOP, 2)
fEnd = dvm.addContextRestore()

dvm.addDestination(fStart, 0, body, 0)
dvm.addDestination(fStart, 1, body, 1)
dvm.addDestination(body, 0, fEnd, 0)

# call
ret = dvm.addSink()
call = dvm.addContextChange(fStart, ret)
pEnd = dvm.addStopInstruction()

dvm.addDestination(ret, 0, pEnd, 0)


test = dvm.addSink()
dvm.addDestination(test, 0, call, 0)
dvm.addDestination(test, 1, call, 1)


tag1 = dvm.token.Tag(0, call, 0, -1)
tag2 = dvm.token.Tag(0, call, 1, -1)
token1 = dvm.token.Token("top", tag1)
token2 = dvm.token.Token("kek", tag2)



# # # function
# pEnd = dvm.addStopInstruction()
# body = dvm.addSink()
# dvm.addDestination(body, 0, pEnd, 0)

# tag1 = dvm.token.Tag(0, body, 0, -1)
# tag2 = dvm.token.Tag(0, body, 1, -1)
# token1 = dvm.token.Token("top", tag1)
# token2 = dvm.token.Token("kek", tag2)

dvm.runtime.start(tokens = [token1, token2])