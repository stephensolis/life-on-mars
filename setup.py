#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='spAIce2018',
    version='0.0.1',
    description='',
    author='spAIce Team',
    author_email='spaice2018@gmail.com',
    url='https://github.com/stephensolis/spAIce2018',
    packages=find_packages(exclude=['tests', '.cache', '.venv', '.git', 'dist']),
    scripts=[],
    install_requires=[
        'opencv-python',
        'scrapy',
        'bs4',
        'requests'
    ]
)