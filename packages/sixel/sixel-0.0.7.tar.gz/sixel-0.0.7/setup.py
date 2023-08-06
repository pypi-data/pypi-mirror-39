import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name='sixel',
	version='0.0.7',
	author='mat',
	author_email='fake@email.lol',
	description='Draw pixels and stuff yay',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://repl.it/@mat1/Sixel',
	packages=setuptools.find_packages(),
	install_requires='Pillow',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)