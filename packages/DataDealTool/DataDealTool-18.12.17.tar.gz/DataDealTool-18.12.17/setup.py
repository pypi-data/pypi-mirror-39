#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   LogTool.py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-11-20
Description:
   setup tool
"""

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)

from setuptools import setup
from setuptools import find_packages

setup(
    name="DataDealTool",
    version="18.12.17",
    keywords=("excel", "Data", "csv", "xlsx"),
    description="The package for csv and excel converting",
    long_description="This package implements the conversion between CSV files and Excel files." +
    		     "dictorder provide ordered Dictionaries and return a Dictionaries too.",
    license="MIT License",

    url="https://github.com/lijiacaigit/DataDealTool",
    author="Lijiacai",
    author_email="1050518702@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["csv", "openpyxl", "pandas", "xlwt", "collections"]  # 这个项目需要的第三方库
)
