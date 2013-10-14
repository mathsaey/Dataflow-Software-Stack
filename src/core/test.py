# Saves a lot of typing on the REPL

from port import *
from edge import *
from literal import *
from abstractnode import *
from operationnode import *
import scheduler

def useless(*ignore):
	print "I'm useless :("

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

outE1 = testNode.addOutput(endPort1)
outE2 = testNode.addOutput(endPort2)
inL1 = Literal(IP1, 1)
inL2 = Literal(IP2, 3)

scheduler.main.run()