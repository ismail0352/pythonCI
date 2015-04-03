#!/usr/bin/python
# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

Get the version string.
"""

from __future__ import print_function

import errno
import json
import sys


def main():
    """
    Reads the build.default.json file, parses it, and prints the version string.

    :return: 0 on success, non-zero on failure.
    """

    infile_name = 'src/config/build.default.json'

    # Open the input file and load it into memory.
    try:
        infile = open(infile_name, 'r')
    except IOError as e:
        if e.errno == errno.ENOENT:
            print("This script must be run from the root of the iris repository.",
                  file=sys.stderr)
        else:
            print("Error: cannot open {0} for reading: {1}".format(infile_name, e.strerror),
                  file=sys.stderr)
        return 1
    build_data = json.load(infile)
    infile.close()

    # Print the version.
    print(build_data['version'])


if __name__ == '__main__':
    sys.exit(main())
