# token.py
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
Tagged token creation

Responsible for the creation and definition of tokens

The following functions can be used by other modules:

createToken(inst, port, cont, datum)
	Create a tagged token.

	inst: The target instruction
	port: A port of this instruction
	cont: The context of this instruction
	datum: The datum this token carries

createLiteral(inst, port, datum)
	Create a literal token.
	Works like createToken but doesn't use
	a context.
"""

import context

# ---------------- #
# Public Functions #
# ---------------- #

def createToken(inst, port, cont, datum):
	tag = Tag(inst, port, cont)
	return Token(datum, tag)

def createLiteral(inst, port, datum):
	tag = LiteralTag(inst, port)
	return Token(datum, tag)

# ----- #
# Token #
# ----- #

class Token(object):
	def __init__(self, datum, tag):
		super(Token, self).__init__()
		self.datum = datum
		self.tag = tag

	def __str__(self):
		tagString = "[" + str(self.tag) + "]"
		dataString = "(" + str(self.datum) + ")"
		return "<| " + dataString + " " + tagString + " |>"

# ---- #
# Tags #
# ---- #

class Tag(object):
	def __init__(self, inst, port, cont):
		super(Tag, self).__init__()
		self.cont = cont
		self.port = port
		self.inst = inst

	def __str__(self):
		inst = str(self.inst) + " | "
		port = str(self.port) + " | "
		return inst + port + str(self.cont)

	def __eq__(self, other):
		return (self.inst == other.inst and
		       self.port == other.port and
		       self.cont == other.cont)

	def isLiteral(self):
		return self.cont == context.literalContext()

class LiteralTag(Tag):
	def __init__(self, inst, port):
		super(LiteralTag, self).__init__(inst, port, context.literalContext())