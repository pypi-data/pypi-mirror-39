import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="xterm",
	version="0.7.3",
	author="mat",
	author_email="fake@email.lol",
	description="Custom keyboard and mouse events for xTerm terminals",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://repl.it/@mat1/Terminal-thing",
	packages=setuptools.find_packages(),
	install_requires='Pillow',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)