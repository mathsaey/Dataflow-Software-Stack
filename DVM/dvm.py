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
import core 
import core.token
import core.memory
import core.runtime

log.setup()

import read

read.parseFile("../examples/simple.dis")
print str(core.memory.memory())

core.memory.reset()


def tOP(a,b):
	return a + b

# entry point
entry = core.addSink()
exit = core.addSink()

# call
ret = core.addSink()
call = core.addContextChange(fStart, ret)
pEnd = core.addStopInstruction()

core.addDestination(ret, 0, pEnd, 0)


# # function
fStart = core.addSink()
body = core.addOperationInstruction(tOP, 2)
fEnd = core.addContextRestore()

core.addDestination(fStart, 0, body, 0)
core.addDestination(fStart, 1, body, 1)
core.addDestination(body, 0, fEnd, 0)



test = core.addSink()
core.addDestination(test, 0, call, 0)
core.addDestination(test, 1, call, 1)
print str(core.memory.memory())


# tag1 = core.token.Tag(0, call, 0, -1)
# tag2 = core.token.Tag(0, call, 1, -1)
# token1 = core.token.Token("top", tag1)
# token2 = core.token.Token("kek", tag2)


#core.runtime.start(tokens = [token1, token2])


##
# \todo
#		Figure out a way to deal with literals
# \todo
#		Stop instruction that can contain tokens until
#		it receives a signal (handle on meta level)
##