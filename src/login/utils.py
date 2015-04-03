# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
 
import json
import logging
import os

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext

from frontend_utils.view_base import ViewBase

logger = logging.getLogger("iris")


def Error404(request):
    """
    When you raise an Http404 exception, Django loads a special view devoted
    to handling 404 errors. By default, it is the view
    django.views.defaults.page_not_found,
    which loads and renders the template 404.mako.

    Args:
        request: represents a single HTTP request. Request objects also have
                 a few useful methods like GET,POST,DELETE etc.

    Returns:
        Renders a 404.mako template with username and session_permission_list
        if username and session_permission_list is blank it does
        not show that details on page.

    Raises:
        None
    """
    try:
        username = request.session['username']
        session_permission_list = request.session['session_permission_list']
    except:
        username = ''
        session_permission_list = []

    return ViewBase.render_template_static(request, '404.mako', username=username, session_permission_list=session_permission_list,)


def Error403(request,error=None):
    """
    When you raise an Http403 exception, Django loads a special view devoted
    to handling 403 errors. By default, it loads and renders the
    template 403.mako.

    Args:
        request: represents a single HTTP request. Request objects also have
                 a few useful methods like GET,POST,DELETE etc.

    Returns:
        Renders a 403.mako template with username and session_permission_list
        if username and session_permission_list is blank it does
        not show that details on page.

    Raises:
        None
    """
    try:
        username = request.session['username']
        session_permission_list = request.session['session_permission_list']
    except:
        username = ''
        session_permission_list = []

    return ViewBase.render_template_static(request, '403.mako', error_message=error, username=username, session_permission_list=session_permission_list,)


def Error400(request):
    """
    When you raise an Http400 exception, Django loads a special view devoted
    to handling 404 errors. By default, it loads and renders the
    template 400.mako.

    Args:
        request: represents a single HTTP request. Request objects also have
                 a few useful methods like GET,POST,DELETE etc.

    Returns:
        Renders a 400.mako template with username and session_permission_list
        if username and session_permission_list is blank it does
        not show that details on page.

    Raises:
        None
    """
    try:
        username = request.session['username']
        session_permission_list = request.session['session_permission_list']
    except:
        username = ''
        session_permission_list = []

    return ViewBase.render_template_static(request, '400.mako', username=username, session_permission_list=session_permission_list,)


def Error401(request):
    """
    When you raise an Http401 exception, Django loads a special view devoted
    to handling 401 errors. By default, it loads and renders the
    template 401.mako.

    Args:
        request: represents a single HTTP request. Request objects also have
                 a few useful methods like GET,POST,DELETE etc.

    Returns:
        Renders a 401.mako template with username and session_permission_list
        if username and session_permission_list is blank it does
        not show that details on page.

    Raises:
        None
    """
    try:
        request.session['access_token']
    except:
        return HttpResponseRedirect('/login/')
    try:
        username = request.session['username']
        session_permission_list = request.session['session_permission_list']
    except:
        username = ''
        session_permission_list = []

    return ViewBase.render_template_static(request, '401.mako', username=username, session_permission_list=session_permission_list,)


def Error500(request, error=None):
    """
    When you raise an Http500 exception, Django loads a special view devoted
    to handling 404 errors. By default, it is the view
    django.views.defaults.server_error,
    which loads and renders the template 500.mako.

    Args:
        request: represents a single HTTP request. Request objects also have
                 a few useful methods like GET,POST,DELETE etc.

    Returns:
        Renders a 500.mako template with username and session_permission_list
        if username and session_permission_list is blank it does
        not show that details on page.

    Raises:
        None
    """
    try:
        username = request.session['username']
        session_permission_list = request.session['session_permission_list']
    except:
        username = ''
        session_permission_list = []

    return ViewBase.render_template_static(request, '500.mako', error_message=error, username=username, session_permission_list=session_permission_list,)

def csrf_failure(request, reason = ""):
     return Error403(request, ugettext("CSRF verification failed: {0}").format(reason))

class InitAPI(object):
    """
    Initialize API attributes

    Attributes:
                    None
    """

    def __init__(self):
        """
        Get attributes from config.json file and stores into the json_data variable

        It initialise some important variables like CLIENTID, CLIENTSECRET, GOOGLE_ANALYTICS,
        baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

        Args:
                None

        Returns:
                None

        Raises:
                None

        """
        if os.path.isfile(settings.CONFIG_PATH):
            config_path = settings.CONFIG_PATH
        else:
            config_path = settings.CONFIG_DEFAULT_PATH
        with open(config_path) as json_data:
            data1 = json.load(json_data)
            json_data.close()
            self.URL = str(data1["URL"])
            self.SUB_URL = str(data1["SUB_URL"])
            self.USERNAME = str(data1["USERNAME"])
            self.PASSWORD = str(data1["PASSWORD"])
            self.CLIENTID = str(data1["CLIENTID"])
            self.CLIENTSECRET = str(data1["CLIENTSECRET"])
            self.GOOGLE_ANALYTICS = str(data1["GOOGLE_ANALYTICS"])
            self.SERVER_TIMEZONE = str(data1["SERVER_TIMEZONE"])

            self.Server_baseUrl = self.URL+self.SUB_URL
            self.baseUrl_login = self.Server_baseUrl+'oauth/token'
            self.baseUrl_jobModify = self.Server_baseUrl + 'rest/jobs/'
            self.baseUrl_configfeaturesModify = self.Server_baseUrl + 'rest/nodes/'
            self.baseUrl_permission = self.Server_baseUrl + 'rest/permissions'
            self.baseUrl_role = self.Server_baseUrl + 'rest/roles'
            self.baseUrl_principal = self.Server_baseUrl + 'rest/principals/'
            self.baseUrl_resetRoles = self.Server_baseUrl + 'rest/roles/reset-default/'

            self.api_version = "?api-version=3"
            self.creds = ("moab-admin", "changeme!")
            self.headers = {'Content-type': 'application/json'}
            self.baseUrl_principalEntity = self.Server_baseUrl + 'rest/diag/health/summary'
            self.changemodeadd = "&change-mode=add"
            self.changemodeset = "&change-mode=set"
            self.changemoderemove = "&change-mode=remove"
            self.baseUrl = self.Server_baseUrl  + "rest/insight/priv/"

    def getgoogleanalytics(self):
        """
        Loads GOOGLE_ANALYTICS from __init__().

        Args:
                        None

        Returns:
                        Returns GOOGLE_ANALYTICS as interger value ('0' OR '1')

        Raises:
        None

        """
        return self.GOOGLE_ANALYTICS
    

    def get_server_timezone(self):
        """
        Loads SERVER_TIMEZONE from __init__().
    
        Args:
                        None
    
        Returns:
                        Returns SERVER_TIMEZONE as string
    
        Raises:
        None
    
        """
        return self.SERVER_TIMEZONE

class APIError:
    """
    This class is used to handle errors at API level and return associated error codes

    Attributes:
            error_template: when error occures it renders to error.html page.
    """
    error_template = "error.html"

    @classmethod
    def error_log(self, ex):
        """
        This method is used to return to error in case token vpn is down
        Need to log this into text file

        Args:
             ex: String/unicode

        Returns:
            Error in case token vpn is down

        Raises:
            None
        """
        # HERE WE ARE ADDING ERROR LOGGING
        logger.error(ex)
        error_message = {}
        error_message['messages'] = "Moab Web Services are not responding. Please contact your administrator"
        return error_message

    @classmethod
    def debug_log(self, db):
        """
        This method is used to return to error in case token vpn is down
        Need to log this into text file

         Args:
             db: String/unicode

        Returns:
            None

        Raises:
            None
        """
        # HERE WE ARE ADDING ERROR LOGGING
        logger.debug(str(db))
        pass

# Currently we are storing the status filters in utils
WORKLOAD_FILTER_STATUS = ["RUNNING", "SUSPENDED", "ELIGIBLE", "BLOCKED", "DEFERRED", "HOLD", "FAILED", "VACATED",
                          "REMOVED", "NONE", "COMPLETED", "STAGING", "NOTQUEUED", "IDLE", "STARTING", "UNKNOWN"]
RESOURCE_FILTER_STATUS = ["FREE", "OFFLINE", "BUSY", "DOWN", "IDLE", "UNKNOWN", "RUNNING", "DRAINED", "FLUSH", "NONE",
                          "RESERVED", "UP"]
