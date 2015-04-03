# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

import json
from datetime import datetime

from django.conf import settings
from django.utils.translation import ugettext


class BuildInfo(object):
    """
    This class handles retrieving build information populated when built.
    """
    def load_build_info(self, request):
        """
        Get build information

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc. Used to
                     access and store build data within the session
        Returns:
                        Dictionary containing build information
        Raises:
                        IOError if neither build file can be opened
        """
        if "build_info" in request.session and request.session["build_info"] is not None:
            return request.session["build_info"]
        try:
            build_info_json = json.load(open(settings.BUILD_INFO_PATH))
        except IOError:
            try:
                build_info_json = json.load(open(settings.BUILD_INFO_DEFAULT_PATH))
            except IOError as exc:
                APIError.error_log(exc)
                raise Exception(ugettext(
                    "Error trying to retrieve build information. Please contact your administrator"))

        request.session["build_info"] = {
            'version': build_info_json.get('version'),
            'changeset': build_info_json.get('changeset'),
            'build_date': self.__parse_epoch_date(build_info_json.get('build_date'))
        }
        return request.session["build_info"]

    @staticmethod
    def __parse_epoch_date(date_field, date_format="%Y-%m-%d %H:%M:%S UTC"):
        if date_field is None:
            return None
        return datetime.utcfromtimestamp(date_field).strftime(date_format)
