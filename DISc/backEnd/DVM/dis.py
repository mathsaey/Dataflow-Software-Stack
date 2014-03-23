# dis.py
# Mathijs Saey
# DISc

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
# \package backEnd.DVM.dis
# \brief dis writer
#
# This module contains an API that allows us to write
# DIS files. 
##

import StringIO

DVM_CHUNKS = 2

##
# This class collects the necessary data
# to generate a DIS string.
#
# It's goal is to facilitate the creation of DIS,
# by containing the necessary strings while doing necessary
# bookkeeping such as keys. It also allows us to generate a tidier
# DIS string by arranging the strings per chunk before printing.
##
class DIS(object):

	##
	# Create a DIS object.
	# This automatically calls addPredefined()
	#
	# \param inputs
	#		The amount of inputs the program will accept.
	##
	def __init__(self, inputs):
		super(DIS, self).__init__()

		## Stores the strings per chunk
		self.memory = [[] for i in xrange(0, DVM_CHUNKS)]

		## Contains the current key per chunk
		self.keys = [0 for i in xrange(0, DVM_CHUNKS)]

		self.addPredefined(inputs)
		self.chunks = DVM_CHUNKS
		self.inputs = inputs

	## Add the standard statements to DIS.
	def addPredefined(self, inputs):
		self.addCommentLine("Program entry and exit point", 0)
		self.addInstruction(0, 'PB', [inputs])
		self.addInstruction(0, 'PE', [])
		self.addNewline(0)

	## Link every output of start to an instruction.
	def linkStart(self, key):
		for i in xrange(0, self.inputs):
			self.addLink((0,0), i, key, i)

	## Link the output of a node to stop.
	def linkStop(self, key):
		self.addLink(key, 0, (0,1), 0)

	##
	# Add a string to a chunk.
	# This string does not influence keys.
	##
	def addString(self, str, chunk):
		lst = self.memory[chunk]
		lst.append(str)

	##
	# Add a string that needs to receive a key
	# in the instruction memory.
	# 
	# \param str
	#		A __format string__ that has room for a
	#		single integer, this means the string should 
	#		contain a single %d. This %d will be replaced
	#		by the received key.
	# \param chunk
	#		The chunk where we place the string.
	#
	# \return
	#		A (chunk, key) pair
	##
	def addKeyedString(self, str, chunk):
		key = self.keys[chunk]
		self.keys[chunk] += 1
		str = str % key

		self.memory[chunk].append(str)
		return (chunk, key)

	## 
	# Convenience function to add 
	# a newline for prettier output.
	##
	def addNewline(self, chunk):
		self.addString('', chunk)

	##
	# Convenience function to add a 
	# comment line for better documented output.
	##
	def addCommentLine(self, comment, chunk):
		self.addString('$ %s' % comment, chunk)

	##
	# Generate a chunk string.
	##
	def createChunk(self, idx):
		return "CHUNK %d" % idx

	##
	# Add an instruction.
	#
	# \param chunk 
	#		The chunk this instruction belongs to.
	# \param type
	#		The instruction type (such as OP)
	# \param args
	#		The other arguments, in a list.
	#		These depend on the type of instruction.
	#
	# \return
	#	The (chunk, key) pair of this instruction.
	##
	def addInstruction(self, chunk, type, args):
		argStr = " ".join(map(str, args))
		ins = "INST %s %s %s" % (type, '%d', argStr)
		return self.addKeyedString(ins, chunk)

	##
	# Add a literal to DIS.
	#
	# \param key 
	# 		A (chunk, instruction) key pair.
	# \param port
	#		The port to send the literal to.
	# \param value
	#		The value of the literal.
	##
	def addLiteral(self, key, port, value):
		str = "LITR %d %d <= %s" % (key[1], port, value)
		self.addString(str, key[0])

	##
	# Add a link to DIS.
	#
	# Links are not dependent on chunks.
	# Currently they are written in the chunk of the
	# from instruction.
	#
	# \param fromKey 
	# 		The from (chunk, instruction) key pair.
	# \param fromPort
	#		The port to send from.	
	# \param toKey 
	# 		The to (chunk, instruction) key pair.
	# \param toPort
	#		The port to send to.
	##
	def addLink(self, fromKey, fromPort, toKey, toPort):
		str = "LINK %d %d %d %d %d %d" % (
			fromKey[0], fromKey[1], fromPort,
			toKey[0], toKey[1], toPort)

		self.addString(str, fromKey[0])

	##
	# Return the DIS string for the current
	# contents of the memories.
	##
	def generate(self):
		buffer = StringIO.StringIO()
		buffer.write('$ Generated by DISc \n\n')

		for i in xrange(0, len(self.memory)):
			buffer.write(self.createChunk(i))
			buffer.write('\n')

			chunk = self.memory[i]
			for str in chunk:
				buffer.write(str)
				buffer.write('\n')

			buffer.write('\n')

		res = buffer.getvalue()
		buffer.close()
		return res