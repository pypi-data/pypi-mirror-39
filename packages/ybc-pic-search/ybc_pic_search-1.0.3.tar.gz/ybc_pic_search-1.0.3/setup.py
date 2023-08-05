#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_pic_search',
      version='1.0.3',
      description='Search The Picture From Baidu By The Keywords.',
      long_description='Search The Picture From Baidu By The Keywords.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'python3', 'recognition'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_pic_search'],
      package_data={'ybc_pic_search': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )