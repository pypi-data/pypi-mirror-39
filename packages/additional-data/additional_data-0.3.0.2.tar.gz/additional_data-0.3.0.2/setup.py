#!/bin/python3
# -*- coding: UTF-8 -*-
#
from setuptools import setup, find_packages
from additional_data import __version__

requirements = ['argparse', 'lxml', 'PyPDF2', 'reportlab']

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='additional_data',
      version=__version__,
      description="Simple library for reading and writing additional data files",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries",
      ],
      author='Andreas Starke',
      url='http://4s4u.de/additional_data/',
      author_email="andreas@4s4u.de",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      additional_data_util = additional_data.additional_data_util:main
      """
      )
