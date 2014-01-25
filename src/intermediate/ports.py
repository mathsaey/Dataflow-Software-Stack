# ports.py
# Mathijs Saey
# dvm

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 		
# of this software and associated documentation files (the "Software"), to deal		      
# in the Software without restriction, including without limitation the rights		
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell		
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

##
# \file ports.py
# \namespace intermediate.ports
# \brief Port definitions
#
# Defines the various port types of IGR
##

##
# Abstract Port
#
# Defines an abstract port, a port is the entry or exit point to any node.
# A port is aware of the node that it belongs to, as well as the index it has in this node.
##
class Port(object):

	##
	# Creates a new port for a node and an index
	#
	# \param node
	#		The node that this port belongs to
	# \param idx
	# 		The index that this node belongs to
	##
	def __init__(self, node, idx):
		super(Port, self).__init__()
		self.node = node
		self.idx = idx

	##
	# Create a string version of the port.
	#
	# \return
	#	A string representing this port.
	# 	This string should not be used to recreate this port.
	##
	def __str__(self):
		name = self.__class__.__name__
		idx = "'" + str(self.idx) + "'"
		node = str(self.node)
		return name + " " + idx + " of " + node

##
# Port that accepts input for a node.
##
class InputPort(Port):

	def __init__(self, node, idx):
		super(InputPort, self).__init__(node, idx)
		self.source = None

	##
	# Attach this port to another port or literal
	# This is an implicit edge representation.
	# 
	# \param source
	#		The source of the connection, a port or literal.
	##
	def attach(self, source):
		self.source = source

##
# Exit point of a node.
#
# An output port can be attached to many input ports of
# other nodes. Any data sent through the port is delivered
# to all of these.
##
class OutputPort(Port):

	def __init__(self, node, idx):
		super(OutputPort, self).__init__(node, idx)
		self.targets = []

	##
	# Add a target to this output port,
	# has to be an input port.
	#
	# \param target
	#		The target to add.
	##
	def addTarget(self, target):
		self.targets.append(target)