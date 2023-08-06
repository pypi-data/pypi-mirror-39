'''
socket extention gui setup file
'''
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()
	

setup(name='sug_sock',
	  version='0.0.5',
      description='suguv socket expantion pack',
	  long_description=long_description,
	  long_description_content_type="text/markdown",
      url='https://bitbucket.org/SuguvHyde/sug_sock/src/master/',
      author='Suguv',
      author_email='orsegev7@gmail.com',
      license='MIT',
      packages=['sug_sock'],
      zip_safe=False)