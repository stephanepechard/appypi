# -*- coding: utf-8 -*-
""" appypi setup.py script """

# appypi
from appypi import __version__
# system
from setuptools import setup
from os.path import join, dirname


setup(name='appypi',
      version=__version__,
      description='appypi: sandboxing apps from Pypi packages',
      author='Stéphane Péchard',
      author_email='stephanepechard@gmail.com',
      packages=['appypi', 'tests'],
      url='http://stephanepechard.github.com/appypi',
      long_description=open('README.txt').read(),
      scripts=['bin/appypi'],
      install_requires=['blessings', 'fabric', 'sqlalchemy'],
      tests_require=['nose'],
      include_package_data=True,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
      ],
)
