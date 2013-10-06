# core.py
# Mathijs Saey
# dvm prototype

import type

def parse_comment(str):
	pass

functions = {
	'C' : parse_comment,
	'T' : type.parse_type
}

def parseString(str):
	lines = str.split("\n")
	for line in lines:
		arr = line.split()
		if len(arr) is not 0:
#			print line
			functions[line[0]](arr)


test = """ 
T 1 1 0    %na=Boolean
T 2 1 1    %na=Character
T 3 1 2    %na=Double
T 4 1 3    %na=Integer
T 5 1 4    %na=Null
T 6 1 5    %na=Real
T 7 1 6    %na=WildBasic
T 8 10
T 9 0	4    %na=intarr
T 10 8	9	0
T 11 3	10	10
T 12 8	4	0
T 13 8	9	12
T 14 3	13	10
T 15 4	4
T 16 8	4	12
T 17 8	9	16
T 18 8	9	17
T 19 3	18	10
T 20 8	9	10
T 21 8	9	20
T 22 3	10	21
T 23 4	1
"""