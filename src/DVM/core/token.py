# token.py
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
# \package core.token
# \brief DVM Tagged tokens
# 
# This module defines the various tokens that 
# carry the state of the program.
##

##
# Represents a DVM token.
# A token carries program data and a Tag.
# The tag contains all the "meta" information about
# the token, such as it's destination and context.
##
class Token(object):
	def __init__(self, datum, tag):
		super(Token, self).__init__()
		self.datum = datum
		self.tag = tag

	def __str__(self):
		tagString = "[" + str(self.tag) + "]"
		dataString = "'" + str(self.datum) + "'"
		return "<| " + dataString + " " + tagString + " |>"

##
# Represents a tag.
# A tag contains the meta information about
# a token.
##
class AbstractTag(object):
	def isSpecial(self):
		raise NotImplementedError("Abstract method")

##
# Standard tag.
# A standard tag contains the destination
# (instruction and port) of a token as well as it's context.
#
# Conceptually, a tag has 2 parts:
# * A static part, it's port and instruction which are part of the program
# * A dynamic part, it's core and context, which are dynamically assigned at runtime.
##
class Tag(object):
	def __init__(self, core, inst, port, cont):
		super(Tag, self).__init__()
		self.core = core
		self.cont = cont
		self.port = port
		self.inst = inst

	def __str__(self):
		core = "core " + str(self.core) + " | "
		inst = "inst " + str(self.inst) + " | "
		port = "port " + str(self.port) + " | "
		cont = "cont " + str(self.cont) 
		return core + inst + port + cont

	def isSpecial(self): return False

##
# Special Tag
#
# Represents a tag that has to be treated 
# differently by the runtime, examples include
# the stop tag, which indicates that the program has to
# terminate upon receiving the token containing this tag.
##
class STag(AbstractTag):
	def __str__(self): return "<STag>"
	def isSpecial(self): return True

##
# Stop Tag
#
# Signals the end of program execution.
##
class StopTag(STag):
	def __str__(self): return "<STOP>"