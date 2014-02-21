# __init__.py
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

##
# \package compiler
# \brief IGR Compiler
# 
# This module defines the compiler that 
# converts IGR into instructions and tokens 
# that can be used by DVM. 
#
# The compiler also performs a few passes on IGR before
# doing so in order to simplify and optimize the produced dataflow.
#
# \todo
#		* Remove all literals
#			* Add as an implicit part of instruction
#			* If all are literals, execute and add as literal to next
#			* Cascade from here
#			* Literal calls should execute the entire function with input
#		* Break down compound nodes.
#			* Collection of standard operations
#			* Express in terms of small amount of instructions
#		* Compile to DVM 
##

from dot import runDot, dotToFile