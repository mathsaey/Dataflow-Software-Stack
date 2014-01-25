# main.py
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

import api

def tOP(a,b):
	return a + b

# function
fStart = api.addForwardInstruction()
body = api.addOperationInstruction(tOP, 2)
fEnd = api.addContextRestoreInstruction()

api.addDestination(fStart, 0, body, 0)
api.addDestination(fStart, 1, body, 1)
api.addDestination(body, 0, fEnd, 0)

# call
ret = api.addForwardInstruction()
call = api.addContextChangeInstruction(ret)
pEnd = api.addStopInstruction()

api.bindCall(call, fStart, fEnd)
api.addDestination(ret, 0, pEnd, 0)

api.addLiteral(call, 0, "top")
api.addLiteral(call, 1, "kek")

api.run()

