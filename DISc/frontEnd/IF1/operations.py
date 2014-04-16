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
# \package frontEnd.IF1.operations
# \brief IF1 operations
#
# This module defines names for the various IF1
# node types.
##

import logging
log = logging.getLogger(__name__)

# ---------------- #
# Function Mapping #
# ---------------- #

operations = {
	100 : 'arrAddBck',
	101 : 'arrAddFrnt',
#	102 : 'AAdjust', # Unknown operation
	103 : 'ABuild',
	104 : 'arrCat',
	105 : 'arrGet',
	106 : 'AFill',
	107 : 'AGather',
	108 : 'arrIsEmpty',
	109 : 'arrBound',
	110 : 'ALimL',
#	111 : 'ARemH',
#	112 : 'ARemL',
	113 : 'arrRepl',
	114 : 'AScatter',
	115 : 'ASetL',
	116 : 'arrLen',
	117 : 'abs',
#	118 : 'BindArguments',
	119 : 'bool',
	120 : 'Call',
	121 : 'string',
	122 : 'div',
	123 : 'float',
	124 : 'equals',
	125 : 'Exp',
#	126 : 'FirstValue',
#	127 : 'FinalValue',
	128 : 'floor',
	129 : 'int',
#	130 : 'IsError',
	131 : 'less',
	132 : 'lessEq',
	133 : 'max',
	134 : 'min',
	135 : 'sub',
	136 : 'mod',
	137 : 'neg',
	138 : 'noOp',
	139 : 'not',
	140 : 'notEq',
	141 : 'add',
	142 : 'range',
#	143 : 'RBuild',
#	144 : 'RElements',
#	145 : 'RReplace',
#	146 : 'RedLeft',
#	147 : 'RedRight',
#	148 : 'RedTree',
#	149 : 'Reduce',
#	150 : 'RestValues',
	151 : 'float',
	152 : 'mul',
#	153 : 'Trunc',
#	154 : 'PrefixSize',
#	155 : 'Error',
#	156 : 'ReplaceMulti',
#	157 : 'Convert',
#	158 : 'CallForeign',
#	159 : 'AElementN',
#	160 : 'AElementP',
#	161 : 'AElementM',
#	170 : 'AAddLAT',
#	171 : 'AAddHAT',
#	172 : 'ABufPartition',
#	173 : 'ABuildAT',
#	174 : 'ABufScatter',
#	175 : 'ACatenateAT',
#	176 : 'AElementAT',
#	177 : 'AExtractAT',
#	178 : 'AFillAT',
#	179 : 'AGatherAT',
#	180 : 'ARemHAT',
#	181 : 'ARemLAT',
#	182 : 'AReplaceAT',
#	183 : 'ArrayToBuf',
#	184 : 'ASetLAT',
#	185 : 'DefArrayBuf',
#	186 : 'DefRecordBuf',
#	187 : 'FinalValueAT',
#	188 : 'MemAlloc',
#	189 : 'BufElements',
#	190 : 'RBuildAT',
#	191 : 'RecordToBuf',
#	192 : 'RElementsAT',
#	193 : 'ReduceAT',
#	19  : ShiftBuffer,
#	195 : 'ScatterBufPartitions',
#	196 : 'RedLeftAT',
#	197 : 'RedRightAT',
#	198 : 'RedTreeAT'
}

def get(label, ctr = "?"):
	key = int(label)
	try:
		func = operations[key]
	except KeyError:
		log.error("Line %s, Undefined function code encountered: %d, using NoOp", ctr, label)
		return 'noOp'
	else: 
		return func
