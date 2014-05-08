# dispatcher.py
# Mathijs Saey
# DVM

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
# \package core.scheduler
# \brief DVM instruction scheduler
#
# This module defines the scheduler.
# The scheduler is responsible for deciding when and how
# to execute an instruction.
##

import logging
log = logging.getLogger(__name__)

##
# DVM Scheduler
#
# Decides when and how to execute an instruction.
##
class Scheduler(object):
	def __init__(self, core):
		super(Scheduler, self).__init__()
		self.core = core
		
	def schedule(self, inst, args):
		try:
			inst = self.core.memory.get(inst)
		except KeyError:
			log.error("Encountered token(s) with faulty destination! %s", args)
		else:
			log.info("Scheduling: %s", inst)
			inst.execute(args, self.core)
