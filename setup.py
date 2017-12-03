import re
from codecs import open
from os import path
from setuptools import find_packages, setup


PACKAGE_NAME = 'peyton'
VERSION = '0.1.6'


setup(name=PACKAGE_NAME,
      author='Ross Taylor',
      author_email='rj-taylor@live.co.uk',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Utilities'],
      description=('Peyton, an API wrapper for the Throne.AI Platform'),
      keywords='throne api wrapper',
      packages=find_packages(exclude=['tests', 'tests.*']),
      license='MIT',
      url='https://throne.ai/',
      version=VERSION)