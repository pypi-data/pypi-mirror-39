import setuptools
	
setuptools.setup(
	name="newsapi-scraper",
	version="0.0.1",
	author="Kirtus Justus",
	author_email="kirtusjustus@outlook.com",
	description="A fork of the newsapi-python repo. Intended to clean up the code for personal use.",
	install_requires=['requests==2.21.0'],
	packages=setuptools.find_packages(),
	keywords=['newsapi','news'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],

)