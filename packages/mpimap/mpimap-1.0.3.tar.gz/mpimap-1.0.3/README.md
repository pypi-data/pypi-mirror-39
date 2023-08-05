# Mpimap

This package is a wrapper for `mpi4py` to allow for the easy running of functions in parallel on a single computer of on multiple nodes of a HPC cluster.

The code used to implement the `mpimap` methods will also function when no `mpi` environment is used, or only a single processor is specified.

## Setup

Once imported, create an instance of the `Mpimap` class:

```
mpi = mpimap.Mpimap()
```

To have each `mpi` process print its information, use:

```
mpi.info()
```

At this point, all `mpi` instance still continue to process all lines within the `script.py` being run or command sent to the interpreter. To put all worker nodes into a "listening" state where they only accept commands sent from the head process, use:

```
mpi.start()
```

From this point, command in the `script.py` running or command sent to the interpreter will only be processed by the head process. To determined the status of each worker process after it has been started, use:

```
mpi.status()
```

To kill all worker nodes once finished, use:

```
mpi.stop()
```

## Functions

To run code on each of the worker nodes once they have being "listening" for jobs, include the code in a function with no arguments and use:

```
mpi.run(func)
```

`Mpimap` include a `map()` function which behaves as the `builtin` version included with python:

```
output = mpi.map(func, args)
```

This will send a copy of the function to all worker nodes, and then queue the args list, sending values to each node not currently running a job. The input order is maintained by the output.

`Mpimap` also includes the function `gmap()`. This is a special instance of `map()` that is intended for running groups of jobs where an argument returning a "failed" state results in all jobs within that group being canceled:

```
output = mpi.gmap(func, args, groupind=0, failstate=None)
```

For this function, `args` is a list of lists. The argument `groupind` determines which entry in each list run by the function is used to determine that jobs group. The argument `failstate` is the value checked to determine if the job was a success or failure.

An addition static function is included called `gmatrix`. This can be used to generate a list of all possible combinations of two lists, and include N number of constants to all combinations:

```
x = [1, 2, 3]
y = [10, 20]
constants = (a, b)
out = mpi.gmatrix(x, y, *constants)
```

Return:

```
>>> out = [
		('0', 1, 10, a, b),
		('1', 1, 20, a, b),
		('2', 2, 10, a, b),
		('3', 2, 20, a, b),
		('4', 3, 10, a, b),
		('5', 3, 20, a, b)]
```

## Example

To test the provided functions and check the difference in processing time between `builtin.map()` and `mpimap.map()`, run:

```mpirun -n <Number of processors you want to use> python test.py```

The full working example is given here:

```
def func_cheap(*args):
	"""Do nothing"""
	return


def func_expensive(n):
	"""Basic factorising problem"""
	factors = set([])
	for i in xrange(n - 1):
		i = i + 1
		# Skip factors
		if i in factors:
			continue
		# Find factors
		if n % i == 0:
			factors.add(i)
			factors.add(n / i)

	return sorted(factors)


# Build mpi
mpi = mpimap.Mpimap(sleep=0, debug=False)
mpi.info()
mpi.start()

# Run function on all nodes
mpi.run(func_cheap)

# Set up function and arguments
args = range(5000, 10000)

# Not in parallel
t0 = time.time()
res = map(func_expensive, args)
dt = time.time() - t0
print '\nNon Parallel: {}'.format(dt)

# Parallel
t0 = time.time()
res = mpi.map(func_expensive, args)
dt = time.time() - t0
print '\nParallel: {}\n'.format(dt)

mpi.stop()
mpi.exit()
```