# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

import os
import sys

path = '/opt/iris'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'iris.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
