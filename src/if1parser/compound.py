# operations.py
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
# \package if1parser.compound
# \brief Compound node reference
# 
# This module maps the IF1 compound nodes to 
# their IGR counterparts.
##

import IGR.node
import tools

## Various IGR compound nodes.
__COMPOUNDS__ = {
	0  : IGR.node.ForallCNode,
	1  : IGR.node.SelectCNode,
	2  : IGR.node.TagCaseCNode,
	3  : IGR.node.LoopACNode,
	4  : IGR.node.LoopBCNode,
	5  : IGR.node.IfThenElseCNode,
	6  : IGR.node.IterateCNode,
	7  : IGR.node.WhileLoopCNode,
	8  : IGR.node.RepeatLoopCNode,
	9  : IGR.node.SeqForallCNode,
	10 : IGR.node.UReduceCNode
}

def getCompound(label, ctr = "?"):
	key = int(label)
	try:
		constructor = __COMPOUNDS__[key]
	except KeyError:
		tools.error("Cannot find compound node with label: " + label, ctr)
	else: 
		return constructor