#!/usr/bin/env python
import os
from setuptools import setup

# paths
directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(directory, 'README.rst')


try:
    long_description = open(readme_path, 'r').read()
except IOError:
    long_description = ''


setup(name='koodous',
      packages=['koodous'],
      version='1.0.0',
      description='Module to interact with Koodous API',
      author='Antonio Sanchez',
      author_email='asanchez@koodous.com',
      license='Apache Version 2',
      url='https://koodous.com/',
      long_description=long_description,
      download_url='https://github.com/Koodous/python-sdk/archive/master.zip',
      keywords=['koodous', 'api', 'sdk', 'python', 'android', 'apk', 'malware'],
      install_requires=["click",
                        "coloredlogs",
                        "humanfriendly",
                        "Pygments",
                        "requests",
                        "androguard",
                        "certifi"],
      entry_points='''
        [console_scripts]
        koocli=koodous.cli:cli
      '''
      )
