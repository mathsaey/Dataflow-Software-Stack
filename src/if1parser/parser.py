# parser.py
# Mathijs Saey
# dvm prototype

import type
import node
import edge
import func

def parse_comment(str):
	pass

functions = {
	'C' : parse_comment,
	'T' : type.parseType,
	'N' : node.parseNode
}

def parseString(str):
	lines = str.split("\n")
	for line in lines:
		arr = line.split()
		if len(arr) is not 0:
#			print line
			functions[line[0]](arr)

def parseFile(loc):
	file = open(loc, 'r')
	parseString(file.read())