#!/usr/bin/env python
import pip
from setuptools import setup

REQUIREMENTS_FILE = 'requirements.txt'


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='koodous-py-iantruslove',
      packages=['koodous'],
      version='0.9',
      description='Module to interact with Koodous API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Ian Truslove',
      author_email='ian.truslove@gmail.com',
      license='Apache Version 2',
      url='https://koodous.com/',
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
