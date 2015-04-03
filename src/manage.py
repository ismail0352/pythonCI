#!/usr/bin/env python
# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iris.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
