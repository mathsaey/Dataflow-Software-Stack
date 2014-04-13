# operations.py
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

##
# \package frontEnd.IF1.compound
# \brief Compound node reference
# 
# This module maps the IF1 compound nodes to 
# their IGR counterparts.
##

import logging
log = logging.getLogger(__name__)

## Various IGR compound nodes.
__COMPOUNDS__ = {
	0  : 'forall',
	1  : 'select',
	2  : 'tagCase',
	3  : 'LoopA',
	4  : 'loopB',
	5  : 'ifThenElse',
	6  : 'iterate',
	7  : 'while',
	8  : 'repeat',
	9  : 'seqForAll',
	10 : 'uReduce'
}

def getCompound(label, ctr = "?"):
	key = int(label)
	try:
		constructor = __COMPOUNDS__[key]
	except KeyError:
		log.error("Line %d: Cannot find compound node with label: %s", ctr, label)
	else: 
		return constructor