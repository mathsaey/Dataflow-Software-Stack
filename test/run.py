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
		print "Compiling", path
		subprocess.check_call([DISC_PATH, path, '-d', DVM_PATH, '-ll', '40'])

	def runDvm(self, path, inputs):
		print "Running", path
		args = [DVM_PATH, path, '-ll', '40']

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

	def test_sort(self): self.abstract('sort',
		[('['
			'50, 92, 29, 63, 88, 3, 33, 49, 52, 27, 32, 86, 73, 97, 100, 49, 37, 86, 87, 76,'
			'50, 51, 95, 14, 89, 35, 39, 6, 93, 61, 55, 15, 12, 35, 39, 45, 24, 20, 19, 34,'
			'33, 39, 75, 80, 33, 41, 8, 89, 37, 99, 23, 69, 21, 98, 16, 91, 64, 40, 89, 67,'
			'91, 13, 18, 3, 42, 69, 75, 42, 12, 48, 53, 58, 8, 57, 70, 97, 11, 1, 74, 71,'
			'78, 57,28, 100, 46, 9, 4, 96, 91, 18, 32, 1, 86, 80, 81, 55, 3, 20, 60, 91,'
			']')],
		('['
			'1, 1, 3, 3, 3, 4, 6, 8, 8, 9, 11, 12, 12, 13, 14, 15, 16, 18, 18, 19, '
			'20, 20, 21, 23, 24, 27, 28, 29, 32, 32, 33, 33, 33, 34, 35, 35, 37, 37, 39, 39, '
			'39, 40, 41, 42, 42, 45, 46, 48, 49, 49, 50, 50, 51, 52, 53, 55, 55, 57, 57, 58, '
			'60, 61, 63, 64, 67, 69, 69, 70, 71, 73, 74, 75, 75, 76, 78, 80, 80, 81, 86, 86, '
			'86, 87, 88, 89, 89, 89, 91, 91, 91, 91, 92, 93, 95, 96, 97, 97, 98, 99, 100, 100'
		']'))

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