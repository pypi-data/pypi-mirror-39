import setuptools


'''from distutils.core import setup'''
with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name              ='nestgo',
    version           ='1.4.0',
    py_modules        =['nestgo'],
    description       ='A simple printer of nested lists',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
     )
