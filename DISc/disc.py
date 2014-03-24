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
import log
import os

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The DIS Compiler")

#argParser.add_argument("path", help = "The path to the file you want to compile.")
argParser.add_argument("-d", "--dvm", help = "The path to DVM.")

argParser.add_argument("-o", "--output", help = "The location of the output file")
argParser.add_argument("-b", "--backEnd", default = 'DVM', help = "The backEnd to use.")
argParser.add_argument("-f", "--frontEnd", type = str, help = "The frontEnd to use.")

argParser.add_argument("-ll", "--logLevel", type = int, default = 0, help = "Specify the log level")

args = argParser.parse_args()

# DEBUG

#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/sort.sis"
loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/select.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/call.sis"
#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/simple.sis"

args.path = loc
# args.logLevel = 0

# ------------- #
# Program Setup #
# ------------- #

log.setup(args.logLevel)
fileName, fileExtension = os.path.splitext(args.path)

frontEnd.setUp(fileExtension, args.frontEnd)
frontEnd.fromFile(args.path)

import IGR
IGR.dot(path="../igr.dot", skipCompound = False)

backEnd.setUp(fileName, args.backEnd, args.output)
backEnd.toFile()
print backEnd.generate()
