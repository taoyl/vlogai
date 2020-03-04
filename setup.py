#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(name='vlogai',
      version=read('vlogai/VERSION').splitlines()[0],
      description='Python package for verilog auto instantiation',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      keywords='Verilog, Auto Instantiation, Vim Plugin, Pyverilog',
      author='Yuliang Tao',
      author_email='nerotao@foxmail.com',
      license='GNU GPL 3.0',
      url='https://github.com/taoyl/vlogai',
      packages=find_packages(),
      package_data={'vlogai': ['VERSION'],},
      install_requires=['pyverilog>=1.2.0']
     )