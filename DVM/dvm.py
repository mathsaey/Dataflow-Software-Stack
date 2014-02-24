#!/usr/bin/env pypy

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
import read
import argparse

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The Dataflow Virtual Machine.")
#argParser.add_argument("path", help = "The path to the DIS file you want to run")
#argParser.add_argument("-i", "--input", action = 'append', help = "A value to pass to the program")
#argParser.add_argument("-c", "--cores", type = int, default = 4, help = "The number of cores to use")
#argParser.add_argument("-ll", "--logLevel", type = int, default = 50, help = "Specify the log level")
args = argParser.parse_args()

args.logLevel = 0
args.path = "../examples/simple.dis"
args.cores = 1
args.input = [1,2]

# -------------------- #
# Starting the program #
# -------------------- #

log.setup(args.logLevel)
read.parseFile(args.path)
core.start(args.cores)

for input in args.input:
	core.addData(int(input))

##
# \todo
#		Figure out a way to deal with literals
# \todo
#		Stop instruction that can contain tokens until
#		it receives a signal (handle on meta level)
##