#!/usr/bin/python
import setuptools

setuptools.setup(name='insertcode',
	version='0.0.8',
	description='extension util for insert different code in the different file type',
	url='http://github.com/jeppeter/insertcode',
	author='jeppeter Wang',
	author_email='jeppeter@gmail.com',
	license='MIT',
	packages=setuptools.find_packages(),
	install_requires=['extargsparse'],
	zip_safe=True,
	classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
