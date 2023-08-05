#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='pocoui_lib',
      version='1.1.2',
      description='pocoui lib for souche-inc airtest project',
      url='',
      author='mizhdi',
      author_email='mizhdi@gmail.com',
      license='MIT',
      platforms = "any",
      install_requires = ["pocoui", "pyyaml"],
      packages = find_packages(),
      zip_safe=False)
