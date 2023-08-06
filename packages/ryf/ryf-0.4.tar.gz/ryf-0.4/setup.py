import setuptools

with open('README.md') as f:
	long_description = f.read()

setuptools.setup(
	name='ryf',
	version='0.4',
	scripts=['bin/ryf'],
	author='Miles Boswell',
	author_email='milesboz@me.com',
	description='A programming language written in python',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/bm20894/ryf',
	packages=setuptools.find_packages(),
	classifiers=['Programming Language :: Python :: 3']
	)