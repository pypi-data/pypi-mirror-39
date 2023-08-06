import setuptools

with open("README.md","r")as fh:
	long_description = fh.read()


setuptools.setup(
	name = 'frtool',
	version= '1.0.1',
	author="Jiaqi Zhang",
     	author_email="jiaqi3899@gmail.com",
     	description="self using package",
     	long_description=long_description,
     	long_description_content_type="text/markdown",
     	url="https://github.com/javatechy/dokr",
     	packages=setuptools.find_packages(),
     	classifiers=[
      	   "Programming Language :: Python :: 3",
      	   "License :: OSI Approved :: MIT License",
      	   "Operating System :: OS Independent",
     	],
)