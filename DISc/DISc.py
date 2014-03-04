#!/usr/bin/env python

# main.py
# Mathijs Saey
# DISc

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
import frontEnd
import compiler.dot

#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/sort.if1"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/select.if1"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/call.if1"
loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/simple.if1"

import log
log.setup(0)

frontEnd.set('IF1')
frontEnd.fromFile(loc)
compiler.dot.runDot(path="../igr.dot", skipCompound = True)