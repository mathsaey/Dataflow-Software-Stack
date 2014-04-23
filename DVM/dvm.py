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

##
# \package dvm
# \brief DVM Main file
#
# This module contains the entry point for DVM. It contains the
# UI code, as well as the command line parser and exit handling.
#
# In short it bundles all the components of DVM together and it 
# allows the user to interact with these components.
##

import log
import sys
import dot
import core
import read
import user
import signal
import argparse
import fileinput
import multiprocessing

# --------------- #
# Signal Handlers #
# --------------- #

## Handle an exit signal.
def handle_exit(signal, frame):
	sys.exit(user.EXIT_INTERRUPT)

## Bind handle_exit to sigint.
signal.signal(signal.SIGINT, handle_exit)

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The Dataflow Virtual Machine.")
argParser.add_argument("path", help = "The path to the DIS file you want to run, - to use stdin")
argParser.add_argument("-i", "--input", action = 'append', help = "A value to pass to the program")
argParser.add_argument("-c", "--cores", type = int, default = multiprocessing.cpu_count(), help = "The number of cores to use")
argParser.add_argument("-ll", "--logLevel", type = int, default = 50, help = "Specify the log level")
argParser.add_argument("--dot", action = "store_true", help = "Generate a dot graph of the program")
argParser.add_argument("--dry_run", action = "store_true", help = "Don't run the program but abort after parsing the dis file.")

args = argParser.parse_args()

#args.logLevel = 0
#args.path = "../test/simple.dis"
args.cores = 1
#args.input = ["1","2", "3", "4"]

# ------------ #
# Program Flow #
# ------------ #

# Set up logging.
log.setup(args.logLevel)

# Parse the input files/stdin.
for line in fileinput.input(args.path):
	read.parseLine(line)

# Generate a dot graph of the program
if args.dot:
	dot.dot()

# Abort if dry_run was specified.
if args.dry_run:
	sys.exit(user.EXIT_OK)

# Abort if we need extra input while 
# stdin is already bound to a pipe.
if args.path == "-":
	if core.getIn() != len(args.input):
		print "Missing input, aborting..."
		sys.exit(user.EXIT_INPUT)

# Print the header text:
if sys.stdout.isatty():
	print "DVM running on {} core(s).".format(args.cores)

# Start the cores.
core.start(args.cores)

# Add command line arguments to runtime.
if args.input:
	for data in args.input:
		data = read.parseValue(data)
		core.addData(data)

while not core.hasIn():
	if sys.stdin.isatty():
		data = raw_input("> ")
	else:
		data = raw_input("reading input for port {}...\n".format(core.getPort()))
	data = read.parseValue(data)
	core.addData(data)