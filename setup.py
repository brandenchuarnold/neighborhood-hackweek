#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='neighborhood-hackweek',
      # the version doesn't matter so much,
      # since it's never published.
      version='0.0.1',
      description='A new flask service that maps home information by neighborhood for Hackweek 12',
      long_description=open('README.md').read(),
      packages=find_packages(),
      # your required eggs should go here. if your service depends on
      # any new eggs, they should be added in this list.
      #
      # NOTE: don't add specific versions here, add it to the concrete
      # platform instead. If you have a specific
      # version requirement for this service, uses ranges instead.
      install_requires=[
          'flask',
          'PyYAML',
          'flask-transmute',
          'setuptools >=0.5',
          'z-logging-formatters',
          'zillowdb'
      ],
      entry_points={
          'console_scripts': [
              'debug=neighborhood_hackweek.debug:debug'
          ]
      }
)
