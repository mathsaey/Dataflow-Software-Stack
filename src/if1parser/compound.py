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
# \file if1parser/compound.py
# \namespace if1parser.compound
# \brief Compound node reference
# 
# This module maps the IF1 compound nodes to 
# their IGR counterparts.
##

import igr.node
import tools

## Various IGR compound nodes.
__COMPOUNDS__ = {
	0  : igr.node.ForallCNode,
	1  : igr.node.SelectCNode,
	2  : igr.node.TagCaseCNode,
	3  : igr.node.LoopACNode,
	4  : igr.node.LoopBCNode,
	5  : igr.node.IfThenElseCNode,
	6  : igr.node.IterateCNode,
	7  : igr.node.WhileLoopCNode,
	8  : igr.node.RepeatLoopCNode,
	9  : igr.node.SeqForallCNode,
	10 : igr.node.UReduceCNode
}

def getCompound(label, ctr = "?"):
	key = int(label)
	try:
		constructor = __COMPOUNDS__[key]
	except KeyError:
		tools.error("Cannot find compound node with label: " + label, ctr)
	else: 
		return constructor