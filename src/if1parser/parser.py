# parser.py
# Mathijs Saey
# dvm prototype

import type
import node
import edge
import func
import tools

def parse_comment(str, ctr):
	pass

functions = {
	'E' : parse_comment,
	'L' : parse_comment,
	'G' : parse_comment,
	'X' : parse_comment,
	'{' : parse_comment,
	'}' : parse_comment,
	'C' : parse_comment,
	'T' : type.parseType,
	'N' : node.parseNode
}

def parseLine(line, ctr = "?"):
	arr = line.split()
	key = line[0]
	try:
		functions[key](arr, ctr)
	except KeyError:
		error = "Unrecognized line type: " + key
		tools.error(error, ctr)
	except Exception, e:
		error = "Exception: '" + str(e) + "' while parsing: '" + line + "'"
		tools.error(error, ctr)

def parseString(str):
	ctr = 1
	lines = str.split("\n")
	for line in lines:
		if len(line) is not 0:
			parseLine(line, ctr)
			ctr += 1

def parseFile(loc):
	file = open(loc, 'r')
	parseString(file.read())