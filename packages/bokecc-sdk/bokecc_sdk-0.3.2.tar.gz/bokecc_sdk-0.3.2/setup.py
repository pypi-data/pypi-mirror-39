# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup

PACKAGE_NAME = 'bokecc_sdk'
PACKAGE_PATH = 'bokecc_sdk'

version = __import__(PACKAGE_PATH).__version__

SHORT_DESCRIPTION = '''SDK for bokecc.'''


def long_description():
    return open(join(dirname(__file__), 'README.md')).read()


def read_requirements(filename):
    with open(filename, 'r') as file:
        return [line for line in file.readlines() if not line.startswith('-')]

requirements = read_requirements('requirements.txt')

setup(name=PACKAGE_NAME,
      version=version,
      author='duoduo369',
      author_email='duoduo3369@gmail.com',
      description= SHORT_DESCRIPTION,
      license='MIT',
      keywords='ccsdk,bokecc,bokecc sdk',
      url='https://github.com/duoduo369/bokecc_sdk',
      download_url='https://github.com/duoduo369/bokecc_sdk/archive/newest.zip',
      packages=[PACKAGE_PATH],
      long_description=long_description(),
      install_requires=requirements,
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.7'],
      zip_safe=False)
