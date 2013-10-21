# Saves a lot of typing on the REPL

from port import *
from edge import *
from literal import *
from callnode import *
from abstractnode import *
from functionnode import *
from operationnode import *
import runtime

def useless(*ignore):
	print "I'm useless :("

def testFunc(a,b):
	print "function called!"
	return a + b

# func(a, b, c, d)
#	x = testFunc(a,b)
#	y = testFunc(b,d)
#	return testFunc(x,y)

# main(a,b,c,d)
# 	func(a,b,c,d)

# NODES
mainNode = CallNode(5,1)
funcNode = FunctionNode(4,1)

runtime.pool.addFunction("foo", funcNode)

addNode1 = OperationNode(2,1, testFunc)
addNode2 = OperationNode(2,1, testFunc)
addNode3 = OperationNode(2,1, testFunc)
endNode = OperationNode(1, 0, useless)

# EDGES
# func to first 2 calls
e1 = Edge(funcNode.getInput(0), addNode1.getInput(0))
e2 = Edge(funcNode.getInput(1), addNode1.getInput(1))
e2 = Edge(funcNode.getInput(2), addNode2.getInput(0))
e3 = Edge(funcNode.getInput(3), addNode2.getInput(1))

# 2 calls to 3rd call
e4 = Edge(addNode1.getOutput(0), addNode3.getInput(0))	
e5 = Edge(addNode2.getOutput(0), addNode3.getInput(1))

# 3rd call to function output, output to end
e6 = Edge(addNode3.getOutput(0), funcNode.getOutput(0))
e7 = Edge(funcNode.getOutput(0), endNode.getInput(0))

# LITERALS
lit = Literal(mainNode.getInput(0), "foo")
lit1 = Literal(mainNode.getInput(1), 1)
lit2 = Literal(mainNode.getInput(2), 2)
lit3 = Literal(mainNode.getInput(3), 3)
lit4 = Literal(mainNode.getInput(4), 4)

#runtime.main.run()