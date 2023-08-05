import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="replit",
	version="1.0.4",
	author="mat",
	author_email="fake@email.lol",
	description="Ho ho ho ha ha, ho ho ho he ha. Hello there, old chum. I’m gnot an gnelf. I’m gnot a gnoblin. I’m a gnome. And you’ve been, GNOMED",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://repl.it/@mat1/replit",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)