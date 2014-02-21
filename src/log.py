# log.py
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
# \package log
# \brief DVM Logging
# 
# Shared logger. The logger is responsible for printing output to the user.
# The logger is also built in such a way to allow multiple processes to use it
# without messing up the output.
#
# Heavy use of multiple processes is the reason for creating our own logger instead
# of using the standard library provided by python.
##

import StringIO
import multiprocessing

##
# Defines the various logging levels.
# These should be accessed by index.
#
# Key | Level | Explanation 
# ----|-------|-------
# 0   | DEBG  | Debug log message, the lowest possible value
# 1   | INFO  | Info log message
# 2   | WARN  | Warning message
# 3   | ERR!  | Signal an error, users should expect things to start going wrong after seeing one of these.
##
__severities__ = [
	"\033[32mDEBG\033[0m",
	"\033[34mINFO\033[0m",
	"\033[33mWARN\033[0m",
	"\033[31mERR!\033[0m"
]

##
# The log that controls access to the output.
##
__logLock__ = multiprocessing.Lock()

##
# Update the lock, this should happen after 
# creating a new process.
##
def setLock(lock):
	global __logLock__
	__logLock__ = lock

##
# Get a reference to the loglock.
##
def getLock():
	return __logLock__

##
# Log a message.
# 
# \param level
#		The idx of the loglevel to use, see __severities__
# \param channel
#		The name of the channel, try to stick to a short name,
#		the channel should represent the part of dvm that is sending
#		the message, such as the runtime or the instruction memory.
# \param message
#		The message to send.
##
def _log(level, channel, *msgLst):
	buffer = StringIO.StringIO()

	buffer.write("[" + __severities__[level] + "]")
	buffer.write("['" + channel + "']")
	buffer.write("\t")

	for el in msgLst:
		buffer.write(str(el))
		buffer.write(" ")

	with __logLock__:
		print buffer.getvalue()

	buffer.close()

## Log a debug severity message
def debg(channel, *msgLst): _log(0, channel, *msgLst)
## Log an information message
def info(channel, *msgLst): _log(1, channel, *msgLst)
## Log a warning message
def warn(channel, *msgLst): _log(2, channel, *msgLst)
## Log an error message
def err(channel, *msgLst):  _log(3, channel, *msgLst)