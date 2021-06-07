#!/usr/bin/env python

from setuptools import setup
import os

long_description = """powerindex calculates some common power indices (related to game theory and political science)
"""

setup(name='powerindex',
    version=os.environ['CI_COMMIT_TAG'],
    description='python library to calculate power indices in weighted voting games',
    author='Maxim Litvak',
    author_email='maxim@litvak.eu',
    url='http://github.com/maxlit/powerindex',
    test_suite='test',
    packages=['powerindex'],
    keywords=['power index','voting','Banzhaf','Shapley','Shubik', 'weighted voting game','game theory', 'political science'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Sociology'
        ],
                                         )

