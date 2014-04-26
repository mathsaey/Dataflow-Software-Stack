#!/usr/bin/env python

# disc.py
# Mathijs Saey
# DISc

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentat ion files (the "Software"), to deal
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
# \package disc
# \brief DISc Main file
#
# This module contains the entry point for DISc. It contains the
# UI code, as well as the command line parser and exit handling.
#
# In short it bundles all the components of DVM together and it 
# allows the user to interact with these components.
##

import argparse
import frontEnd
import backEnd
import IGR
import log
import sys
import os

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The DIS Compiler")

argParser.add_argument("path", help = "The path to the file you want to compile.")
argParser.add_argument("-d", "--dvm", help = "The path to DVM.")
argParser.add_argument("-o", "--output", help = "The location of the output file")
argParser.add_argument("-b", "--backEnd", default = 'DVM', help = "The backEnd to use.")
argParser.add_argument("-f", "--frontEnd", type = str, help = "The frontEnd to use.")
argParser.add_argument("-ll", "--logLevel", type = int, default = 30, help = "Specify the log level")

argParser.add_argument("--dot", action = "store_true", help = "Generate a dot graph of the program")
argParser.add_argument("--dry_run", action = "store_true", help = "Don't compile the program but abort after parsing the input file.")

args = argParser.parse_args()

#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/sort.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/select.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/call.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/simple.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/factorial.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/trivial.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/test/forin.sis"
#args.path = loc

# ------------- #
# Program Setup #
# ------------- #

log.setup(args.logLevel)

fileName, fileExtension = os.path.splitext(args.path)

frontEnd.setUp(fileExtension, args.frontEnd)
frontEnd.fromFile(args.path)

if args.dot:
	IGR.dot(skipCompound = False)

if args.dry_run:
	sys.exit(0)

backEnd.setUp(fileName, args.backEnd, args.output)
backEnd.toFile()

