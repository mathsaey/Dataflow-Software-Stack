# Saves a lot of typing on the REPL

from port import *
from edge import *
from literal import *
from abstractnode import *
from operationnode import *

def useless():
	pass

def testFunc(a,b):
	print "function called!"
	return a + b


endNode1 = OperationNode(1,useless)
endNode2 = OperationNode(1,useless)
endPort1 = endNode1.getInput(0)
endPort2 = endNode1.getInput(0)

testNode = OperationNode(2,testFunc)
IP1 = testNode.getInput(0)
IP2 = testNode.getInput(1)

outE1 = Edge(testNode, endPort1)
outE2 = Edge(testNode, endPort2)
inL1 = Literal(IP1, 1)
inL2 = Literal(IP2, 3)
