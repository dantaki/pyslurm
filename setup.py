from setuptools import setup
setup(
	name='pyslurm',
	version='0.0.1',
	url='https://github.com/dantaki/pyslurm',
	author='Danny Antaki',
	author_email='dantaki@ucsd.edu',
	packages=['pyslurm'],
	package_dir={'pyslurm': 'pyslurm/'},
	include_package_data=True,
	scripts= ['pyslurm/pyslurm']
)
