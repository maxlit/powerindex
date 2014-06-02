#!/usr/bin/env python

from distutils.core import setup

long_description = """Example Packages do this and that
"""

setup(name='powerindex',
    version='0.0.4',
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

