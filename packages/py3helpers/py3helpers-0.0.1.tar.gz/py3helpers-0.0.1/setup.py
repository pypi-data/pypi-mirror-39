#!/usr/bin/env python3
"""Create setup script for pip installation of python_utils"""
########################################################################
# File: setup.py
#  executable: setup.py
#
# Author: Andrew Bailey
# History: 12/09/17 Created
########################################################################

import sys
from timeit import default_timer as timer
from setuptools import setup


def main():
    """Main docstring"""
    start = timer()
    setup(
        name="py3helpers",
        version='0.0.1',
        description='Python utility functions',
        url='https://github.com/adbailey4/python_utils',
        author='Andrew Bailey',
        author_email='andbaile@ucsc.com',
        packages=['py3helpers'],
        install_requires=['mappy>=2.14',
                          'biopython>=1.68',
                          'pysam>=0.15',
                          'numpy>=1.14.2'],
        zip_safe=True
    )

    stop = timer()
    print("Running Time = {} seconds".format(stop-start), file=sys.stderr)


if __name__ == "__main__":
    main()
    raise SystemExit
