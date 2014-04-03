#!/usr/bin/env python

# run.py
# Mathijs Saey
# DVM tests

# This file compiles and runs the various example files

import unittest
import subprocess

DVM_PATH  = "../DVM/dvm.py"
DISC_PATH = "../DISc/disc.py"

class Test(unittest.TestCase):

	def compile(self, path):
		subprocess.check_call([DISC_PATH, path, '-d', DVM_PATH, '-ll', '40'])

	def runDvm(self, path, inputs):
		args = [DVM_PATH, path]

		for e in inputs:
			args.append("-i")
			args.append(str(e))

		return subprocess.check_output(args).strip()

	def abstract(self, name, inputs, expected):
		self.compile(name + '.sis')
		res = self.runDvm(name + '.dis', inputs)
		self.assertEqual(res, expected)

	def test_fac(self): self.abstract('factorial', ['5'], '120')
	def test_fib(self): self.abstract('fibonacci', ['10'], '55')
	def test_call(self): self.abstract('call', ['1', '2'], '15')
	def test_simple(self): self.abstract('simple', ['1', '2', '3', '4'], '10')

	def test_select(self): 
		self.compile('select.sis')

		in_out = [
			(['5', '2'], '3'),
			(['0', '2'], '4'),
			(['1', '2'], '3')
		]

		for pair in in_out:
			res = self.runDvm('select.dis', pair[0])
			self.assertEqual(res, pair[1])






unittest.main()

