"""
Parallel function mapping using mpi4py

:author:
	Jed Hollom
:date:
	November 2018
"""

# Standard
import sys
import os
import multiprocessing
import time
# Mpi
from mpi4py import MPI as mpi
import dill
mpi.pickle.dumps = dill.dumps
mpi.pickle.loads = dill.loads


class Mpimap(object):

	def __init__(self, sleep=0.1, debug=False):
		"""
		Parallel function mapping using mpi4py

		:param float sleep: Time between worker processor polling for jobs
		:param bool debug: Toggles printing of debug info
		"""

		# mpi setup
		self.comm = mpi.COMM_WORLD
		self.size = self.comm.Get_size()
		self.rank = self.comm.Get_rank()
		self.type = {True: 'header', False: 'worker'}[self.rank == 0]
		# Use mpi check
		self.usempi = self.size != 1
		# other variables
		self.hostname = mpi.Get_processor_name()
		self.cpu = multiprocessing.cpu_count()
		self.debug = debug
		self.sleep = sleep
		# non mpi check
		self.usempi = self.size != 1
		# function
		self.path = os.getcwd()
		self.function = None

	# --------------------------------------------------------------------------------

	def info(self):
		"""
		print mpi instance info
		"""
		output = '{} | {} | '.format(self.hostname, self.type)
		output = output + 'rank: {}/{} | '.format(self.rank, self.size - 1)
		output = output + 'cpu: {}'.format(self.cpu)
		print output

	def start(self):
		"""
		Put workers into wait state listening for commands
		"""
		if self.type != 'worker':
			return
		if self.usempi is False:
			return

		self._dprint('STARTING')
		status = mpi.Status()
		command = ''

		while True:
			# Wait for message
			self._dprint('Waiting...')
			while not self.comm.Iprobe(source=0):
				time.sleep(self.sleep)

			# Receive data
			data = self.comm.recv(source=0, tag=mpi.ANY_TAG, status=status)

			# Check stop
			if data == 'STOP':
				self._dprint('STOPPING')
				sys.exit()

			# Check ping
			if data == 'PING':
				print 'Node {} running'.format(self.rank)
				continue

			# Check function
			if data == 'FUNC':
				self.function = self.comm.bcast(self.function, root=0)
				self._dprint('Setting function {}'.format(self.function))
				continue

			# Check dir
			if data == 'PATH':
				self.path = self.comm.bcast(self.path, root=0)
				self._dprint('Setting path {}'.format(self.path))
				os.chdir(self.path)
				continue

			# Check run
			if data == 'RUN':
				command = self.comm.bcast(command, root=0)
				self._dprint('Running function {}'.format(command))
				command()
				continue

			# Compute function
			self._dprint('Evaluating input {}'.format(data))
			result = self.function(data)
			self.comm.isend(result, dest=0, tag=status.tag)

	def stop(self):
		"""
		kill all worker processes
		"""
		if self.type != 'header':
			return
		if self.usempi is False:
			return

		for i in range(1, self.size):
			self.comm.send('STOP', dest=i, tag=i)

	# --------------------------------------------------------------------------------

	def map(self, func, args):
		"""
		Run task with input arguments (balanced)

		:param func func: Function to be mapped
		:param list args: list of lists of arguments required by func
		:return list: list of function output object
		"""
		if self.type != 'header':
			return
		if self.usempi is False:
			results = map(func, args)
			return results

		# Data structures
		results = []
		todo = range(0, len(args))
		status = mpi.Status()
		self.function = func

		# Path
		if self.path != os.getcwd():
			self.path = self.comm.bcast(os.getcwd(), root=0)
			for i in range(1, self.size):
				self.comm.send('PATH', dest=i, tag=i)

		# Function
		self.function = self.comm.bcast(self.function, root=0)
		for i in range(1, self.size):
			self.comm.send('FUNC', dest=i, tag=i)

		# Initial jobs
		size = min((self.size - 1), len(args))
		for i in xrange(size):
			self.comm.send(args[i], dest=i + 1, tag=i)
			todo.pop(0)

		# Other jobs
		while len(results) != len(args):
			# Get response
			result = self.comm.recv(source=mpi.ANY_SOURCE, tag=mpi.ANY_TAG, status=status)
			worker = status.source
			i = status.tag
			# Send new job
			if len(todo) != 0:
				self.comm.isend(args[todo[0]], dest=worker, tag=todo[0])
				todo.pop(0)
			# collect jobs
			results.append([i, result])

		# Return
		results = zip(*sorted(results))[1]
		return results

	def gmap(self, func, args, groupind=0, failstate=None):
		"""
		Run task with input arguments (balanced)
		Monitor for failstate and cancel/fail all jobs in group

		:param func func: Function to be mapped
		:param list args: List of lists of arguments required by func
		:param ind groupind: Args index to group by
		:param failstate: object used to determin failed job
		:return list: list of function output object
		"""
		if self.type != 'header':
			return
		if self.usempi is False:
			results = map(func, args)
			return results

		# Data structures
		results = []
		todo = range(0, len(args))
		status = mpi.Status()
		self.function = func

		# Path
		if self.path != os.getcwd():
			self.path = self.comm.bcast(os.getcwd(), root=0)
			for i in range(1, self.size):
				self.comm.send('PATH', dest=i, tag=i)

		# Function
		self.function = self.comm.bcast(self.function, root=0)
		for i in range(1, self.size):
			self.comm.send('FUNC', dest=i, tag=i)

		# Initial jobs
		size = min((self.size - 1), len(args))
		for i in xrange(size):
			self.comm.send(args[i], dest=i + 1, tag=i)
			todo.pop(0)

		# Other jobs
		while len(results) != len(args):
			# Get response
			result = self.comm.recv(source=mpi.ANY_SOURCE, tag=mpi.ANY_TAG, status=status)
			worker = status.source
			i = status.tag
			results.append([i, result])
			# Check failstate
			if result == failstate:
				fid = args[i][groupind]
				fjobs = [x for x in todo if args[x][groupind] == fid]
				[todo.remove(x) for x in fjobs]
				[results.append([x, None]) for x in fjobs]
			# Send new job
			if len(todo) != 0:
				self.comm.isend(args[todo[0]], dest=worker, tag=todo[0])
				todo.pop(0)

		# Return
		results = zip(*sorted(results))[1]
		return results

	def run(self, func):
		"""
		Run a function on all nodes

		:param func func: Function to run
		"""
		if self.type != 'header':
			return
		if self.usempi is False:
			return

		func = self.comm.bcast(func, root=0)
		for i in range(1, self.size):
			self.comm.send('RUN', dest=i, tag=i)

	def status(self):
		"""
		Print status of all nodes to the console
		"""
		if self.type != 'header':
			return
		if self.usempi is False:
			return

		# Send command
		for i in range(1, self.size):
			self.comm.send('PING', dest=i, tag=i)

	# --------------------------------------------------------------------------------

	def _dprint(self, string):
		"""Checks if debug is on and prints statement if true"""
		if self.debug is True:
			print '{} {}: {}'.format(self.type, self.rank, string)

	@staticmethod
	def gmatrix(x, y, *const):
		"""
		Generate all combinations of input variables with added
		constants and iid number string.

		Example
		=======
		x = [1, 2, 3]
		y = [10, 20]
		const = (a, b)
		return [
			('0', 1, 10, a, b),
			('1', 1, 20, a, b),
			('2', 2, 10, a, b),
			('3', 2, 20, a, b),
			('4', 3, 10, a, b),
			('5', 3, 20, a, b)]

		:param list x: list of objects
		:param list y: list of objects
		:param args const: Additional args to be added to all combinations
		:return list: All possible combinations of inputs with const args
		"""
		iid = 0
		output = []
		for i in x:
			for j in y:
				out = (str(iid), i, j) + const
				output.append(out)
				iid = iid + 1

		return output
