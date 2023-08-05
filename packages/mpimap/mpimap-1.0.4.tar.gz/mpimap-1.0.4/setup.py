import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(
	name='mpimap',
	version='1.0.4',
	description='Parallel function mapping using mpi4py',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='http://gitlab.com/Wokpak/mpimap',
	author='Jed Hollom',
	author_email='Jedhollom@gmail.com',
	packages=setuptools.find_packages(),
	install_requires=['multiprocessing', 'mpi4py', 'dill'],
	classifiers=[
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"],
	zip_safe=False)
