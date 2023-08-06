from setuptools import setup, find_packages

setup(
   name='AutoDiff_207_15',
   version='1.0',
   description='Autodifferentiation package',
   author='CS207 group 15',
   packages=find_packages(),  #same as name
   install_requires=['numpy'], #external packages as dependencies
   data_files = [("", ["LICENSE"])],
)
