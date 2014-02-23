# main.py
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

import log
import DVM 
import DVM.token
import DVM.runtime

def tOP(a,b):
	return a + b

# # function
fStart = DVM.addSink()
body = DVM.addOperationInstruction(tOP, 2)
fEnd = DVM.addContextRestore()

DVM.addDestination(fStart, 0, body, 0)
DVM.addDestination(fStart, 1, body, 1)
DVM.addDestination(body, 0, fEnd, 0)

# call
ret = DVM.addSink()
call = DVM.addContextChange(fStart, ret)
pEnd = DVM.addStopInstruction()

DVM.addDestination(ret, 0, pEnd, 0)


test = DVM.addSink()
DVM.addDestination(test, 0, call, 0)
DVM.addDestination(test, 1, call, 1)


tag1 = DVM.token.Tag(0, call, 0, -1)
tag2 = DVM.token.Tag(0, call, 1, -1)
token1 = DVM.token.Token("top", tag1)
token2 = DVM.token.Token("kek", tag2)

DVM.runtime.start(tokens = [token1, token2])
