#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_tel',
      version='1.0.6',
      description='Search the location of mobile phone number.',
      long_description='TSearch the location of mobile phone number.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'phone number', 'search'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_tel'],
      package_data={'ybc_tel': ['*.py']},
      license='MIT',
      install_requires=['ybc_config', 'requests', 'ybc_exception']
     )