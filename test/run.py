#!/usr/bin/env pypy

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
	def test_call(self): self.abstract('call', ['1', '2'], '21')
	def test_simple(self): self.abstract('simple', ['1', '2', '3', '4'], '10')
	def test_trivial(self): self.abstract('trivial', [], '8')
	def test_forin(self): self.abstract('forin', 
		['5', '10', '[5, 10, 30, 3, 40]', '[4, 20, 5]'],
		'[13, 11, 12, 13, 12, 45, 55, 35, 20, 21, 22, 23, 24, 25]')

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