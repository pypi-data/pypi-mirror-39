from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="ImageJudgement",
    version="1.0",
    author="LancerWu",
    author_email="wuxs231@163.com",
    description="command line tool for loop check images",
    url="https://github.com/wuxs231",
    keywords=['images', 'check', 'tool', 'loop'],
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'PIL',
        'os',
    ]
)