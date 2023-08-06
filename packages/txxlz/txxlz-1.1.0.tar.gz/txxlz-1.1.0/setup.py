import pathlib
from setuptools import setup
import os

#The dir containing this file
HERE = os.getcwd()

#the of the README
README = "Simple Python Tools"
with open(os.path.join(HERE, "README.md")) as fh:
	README = fh.read()
	fh.close()

__version__="1.1.0"
#This call to setup does all the work
setup(name="txxlz",
	version="1.1.0",
	description="Simple Small Python tools",
	long_description=README,
	long_description_content_type="text/plain",
	url="https://github.com/ignertic/txxlz",
	author="Gishobert (SuperCode) Gwenzi",
	author_email="ilovebugsincode@gmail.com",
	licence="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent"],
	packages=["txxlz"],
	include_package_data=True,
	install_requires=["requests"],
	entry_points={"console_scripts" : ["txxlz=txxlz.__main__:main"]},
	)