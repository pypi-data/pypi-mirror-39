import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(name="mrequests",version="0.0.6",author="Danie Britto",author_email="dannybritto96@gmail.com",long_description = long_description,long_description_content_type="text/markdown",packages=setuptools.find_packages(),url="https://github.com/dannybritto96/mrequests",classifiers = ["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent"],)
