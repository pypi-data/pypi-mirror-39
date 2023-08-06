# -*- coding: utf-8 -*-
# read https://packaging.python.org/tutorials/packaging-projects/
# run it with:
#   setup.py sdist bdist_wheel
#   twine upload --repository-url https://pypi.org/legacy/ dist/*


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ADTthious", # because ADT already exist
    version="0.2",
    description='Abstract Data Types for python',
    author='Thierry Hervé',
    author_email='thious.rv@gmail.com',
    url="https://github.com/gitthious/ADT.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[], # setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)

