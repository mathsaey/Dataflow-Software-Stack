# parser.py
# Mathijs Saey
# dvm prototype

import type
import edge
import graph
import tools

def parse_comment(str, ctr):
	pass

functions = {
	'C' : parse_comment,
	'T' : type.parseType,
	'E' : edge.parseEdge,
	'L' : edge.parseLiteral,
	'N' : graph.parseNode,
	'G' : graph.parseGraph,
	'X' : graph.parseGraphDef,
	'{' : graph.parseCompoundStart,
	'}' : graph.parseCompoundEnd
}

def parseLine(line, ctr = "?"):
	arr = line.split()
	key = line[0]
	try:
		func = functions[key]
	except KeyError:
		error = "Unrecognized line type: " + key
		tools.error(error, ctr)
	#except Exception, e:
	#	error = "Exception: '" + str(e) + "' while parsing: '" + line + "'"
	#	tools.error(error, ctr)
	else:
		func(arr, ctr)

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