#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.md', 'r') as fr:
    long_description = fr.read()
    
import rm_rspace

setuptools.setup(
    name='rm_rspace',
    version=rm_rspace.__version__,
    license='MIT',
    description='Remove trailing white spaces from a text file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Masashi Takahashi',
    url='https://github.com/masshash/rm_rspace',
    py_modules=['rm_rspace'],
    entry_points={
        'console_scripts': [
            'rm_rspace=rm_rspace:main',
        ],
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
