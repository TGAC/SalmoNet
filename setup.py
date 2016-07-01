#!/usr/bin/env python3
from setuptools import setup

setup(name='SalmoNetWeb',
      version='0.1',
      description='Website for SalmoNet project',
      url='https://github.com/TGAC/SalmoNet',
      author='David Fazekas',
      author_email='Fazekasda@gmail.com',
      license='MIT',
      packages=['SalmoNetWeb'],
      install_requires=[
          'invoke==0.13.0',
      ],
      zip_safe=False
)
