# This file can be used to add multiple view classes. Ex generic or custom views. Currently using basic generic view (django.views.generic.detail.View)

from datetime import datetime, timedelta
import logging
import os
import re

from django.conf import settings
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import View
from mako.lookup import TemplateLookup
import pytz

from api.build_info import BuildInfo


tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__), "..", "tpls"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "configuration"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "nodes"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "jobs"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "error")], default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8')
log = logging.getLogger('iris')


class ViewBase(View):
    """
    This class is the base view class for frontend views. It will allow you to override
    view requests or make changes globally.
    """
    __view_request = None
    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch method for this view. This will get called on each frontend view request before the view methods will be called.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            View being rendered

        Raises:
            None

        """
        self.__view_request = request
        return super(ViewBase, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def add_global_vars(request):
        global_dict = {}
        #add build info
        build_info = BuildInfo()
        global_dict["build_info"] = build_info.load_build_info(request)

        #add csrf token
        global_dict["csrftoken"] = unicode(csrf(request)['csrf_token'])
        return global_dict

    def render_template(self,template_name, response_status_code=200, content_type=None, mimetype=None, **template_data):
        if template_name is None:
            raise Exception("Template name not specified.")
        tpl = tpl_lookup.get_template(template_name)
        template_data.update(self.add_global_vars(self.__view_request))
        return HttpResponse(tpl.render(**template_data), status=response_status_code, content_type=content_type, mimetype=mimetype)
    @staticmethod
    def render_template_static(request, template_name, response_status_code=200, content_type=None, mimetype=None, **template_data):
        if template_name is None:
            raise Exception("Template name not specified.")
        tpl = tpl_lookup.get_template(template_name)
        template_data.update(ViewBase.add_global_vars(request))
        return HttpResponse(tpl.render(**template_data), status=response_status_code, content_type=content_type, mimetype=mimetype)
    def render_template_obj(self,template_name, template_obj, response_status_code=200, content_type=None, mimetype=None):
        if template_name is None:
            raise Exception("Template name not specified.")
        tpl = tpl_lookup.get_template(template_name)
        template_obj.update(self.add_global_vars(self.__view_request))
        return HttpResponse(tpl.render(**template_obj), status=response_status_code, content_type=content_type, mimetype=mimetype)
    def redirect_to_name(self,url_pattern_name,*args,**kwargs):
        if url_pattern_name is None:
            raise Exception("Url pattern name must be specified.")
        url = reverse(url_pattern_name)
        return self.redirect(url,*args,**kwargs)

    def redirect(self,url,*args,**kwargs):
        if url is None:
            raise Exception("Url must be specified.")
        return HttpResponseRedirect(url,*args,**kwargs)

    def redirect_prev(self,*args,**kwargs):
        try:
            path_prev = self.__view_request.session["path_previous"]
            return self.redirect(path_prev,*args,**kwargs)
        except:
            raise Exception("Trying redirect to previous page but previous path does not exist in the session.")


def get_timezone_offset(javascript_timestr, server_timezone):
    """
    Given a time string returned by the JavaScript toTimeString() method,
    return the timezone portion as a string in the format "GMT+NNNN" or
    "GMT-NNNN", where NNNN is a zero-padded integer indicating the hours
    and minutes that local time is offset from UTC.
    
    If the required format is also not satisfied for offset, then the server
    timezone shall be considered to calculate the offset
    
    If timezone is an empty string, then fetch the configured server
    timezone and calculate the timezone offset string similar to what
    is described above, except in place of GMT there will be the standard
    abbreviation of the timezone such as "CET" or "CEST".
    
    If timezone is not a string, then fetch settings.TIME_ZONE and calculate
    its timezone offset string as described above.
    
    Parameters:
        javascript_timestr:  A string containing the current time
                  returned from this JavaScript code run in the browser:
                       (new Date()).toTimeString();
        server_timezone: timezone of the server,  saved in config.json file      
    
    Return value:
        A string containing a timezone offset in the format "AAA+HHMM" or
        "AAA-HHMM". AAA is a standard timezone abbreviation such as "GMT",
        "CET", "CEST", etc. HHMM is a zero-padded integer indicating the
        hours and minutes that local time is offset from UTC.
        Example: "GMT-0400"
    """
    if javascript_timestr:
        valid_offset = re.search(r'[A-Z]{3}\W+\d+',javascript_timestr)
        if valid_offset:
            timezone_offset = (valid_offset).group(0)
        else:
            timezone_offset =  pytz.timezone(server_timezone).localize(datetime.now()).strftime('%Z%z')
    elif javascript_timestr == "":
        timezone_offset =  pytz.timezone(server_timezone).localize(datetime.now()).strftime('%Z%z')
    else:
        timezone_default = settings.TIME_ZONE
        timezone_offset =  pytz.timezone(timezone_default).localize(datetime.now()).strftime('%Z%z')
    return timezone_offset

def local_2_utc(local_time,timezone_offset):
    """
    Given a time string [mainly from filter section like StartDate , EndDate etc]
    gets converted to UTC before it is appended to the view as query.
    
    Time string format from application would be in "YYYY-mm-dd hh:mm:ss" 
    
    Depending upon the timezone_offset , the given time shall be converted to UTC.
    
    Parameters:
        local_time:  A time string in the format "YYYY-mm-dd hh:mm:ss"
        timezone_offset: Difference between UTC and Local time-zone in format "AAA+HHMM"
        or "AAA-HHMM" 
    
    Return value:
        local_time converted to the UTC timezone, as a datetime object. 
    """
    offset = re.search(r'\d+',str(timezone_offset)).group(0)
    deviation = re.search(r'\W',str(timezone_offset)).group(0)
    localTime = datetime.strptime(str(local_time), "%Y-%m-%d %H:%M:%S")
    if deviation == '+':
        utcTime = localTime - timedelta(hours = int(offset[0:2]) ,minutes = int(offset[2:4]))
    if deviation == '-':
        utcTime  = localTime + timedelta(hours = int(offset[0:2]) ,minutes = int(offset[2:4]))
    return utcTime
    

def utc_2_local(utc_time,timezone_offset):
    """
    All the date time format received from the API are in UTC format like 
    "YYYY-mm-dd hh:mm:ss UTC" 
        
    This function converts utc time to local time depending on the timezone_offset 
    
    Parameters:
        utc_time:  A time string in the format "YYYY-mm-dd hh:mm:ss" . The UTC date time 
            received from the API with its "UTC" word trimmed at the end.
        timezone_offset: Difference between UTC and Local time-zone in format "AAA+HHMM"
        or "AAA-HHMM" 
    
    Return value:
         utc_time converted to the local time, as a datetime object.
    """
    offset = re.search(r'\d+',str(timezone_offset)).group(0)
    deviation = re.search(r'\W',str(timezone_offset)).group(0)
    utcTime = datetime.strptime(str(utc_time), "%Y-%m-%d %H:%M:%S")
    if deviation == '+':
        localTime = utcTime + timedelta(hours = int(offset[0:2]) ,minutes = int(offset[2:4]))
    if deviation == '-':
        localTime = utcTime - timedelta(hours = int(offset[0:2]) ,minutes = int(offset[2:4]))
    return localTime


def secured(function):
    def wrap(request, *args, **kwargs):
        if "access_token" in request.request.session and request.request.session['access_token'] is not None:
            return function(request, *args, **kwargs)
        else:
            request.request.session['path_previous'] = request.request.path
            return HttpResponseRedirect(reverse('login'))
    return wrap
