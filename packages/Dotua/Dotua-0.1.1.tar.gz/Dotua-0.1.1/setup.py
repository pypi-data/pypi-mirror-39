import setuptools

with open("docs/documentation.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='Dotua',
	version='0.1.1',
	description='Package for Forward/Reverse Autodifferentiation',
	author='Nick Stern, Vincent Viego, Summer Yuan, Zach Wehrwein',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=['Dotua'],
	install_requires=[
	  'numpy',
	  'scipy'
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	url="https://github.com/VV-NS-CY-ZW-CS-207-Organization/cs207-FinalProject",
	license="MIT",
)