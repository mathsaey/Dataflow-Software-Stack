# dvm.py
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
# \package dvm
# \brief dvm interface
#
# This module provides a few convenient shorthands
# for calling DVM.
##

import subprocess

##
# Parse the result that DVM returns.
#
# \param str
#		The result, in string form.
# \return
#		The python version of the result.
##
def parseOutput(str):
	return eval(str)

##
# Run DVM on a dis string, with inputs,
# and return the results.
#
# \param dvmPath
#		The path to dvm, if dvm is not in your system PATH
# \param inputs
#		The list of inputs to pass to dvm
# \param dis
#		A string containing the dis representation of the code to execute.
# \param cores
#		The amount of cores to use when running dvm.
# \param logLevel
#		The loglevel to pass to DVM (useful for debugging)
#
# \return
#		The output returned by dvm, as a python object.
##
def runDVM(dvmPath = "dvm", inputs = [], dis = None, cores = 1, logLevel = 50):
	args = [dvmPath, "-", "-c", str(cores), "-ll", str(logLevel)]

	for e in inputs:
		args.append("-i")
		args.append(str(e))

	dvm = subprocess.Popen(args, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	res = dvm.communicate(dis)
	return parseOutput(res[0])