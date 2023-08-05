from setuptools import setup  ,find_packages
import webfile
import sys

# help(find_packages)
setup(name='webfile',   
      version=webfile.__version__,    
      description='My pypi module',    
      author='Blacksong',    
      author_email='blacksong@yeah.net',       
      url='https://github.com/blacksong',
      packages=find_packages(include=['*','*.html']), 
      classifiers = ["Programming Language :: Python :: 3","Operating System :: OS Independent","Topic :: Software Development :: Libraries :: Python Modules"],
)   
