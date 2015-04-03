# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import logging
import os

from django.conf import settings
from django.middleware.csrf import rotate_token
from django.utils.translation import ugettext as _
from mako.lookup import TemplateLookup

from api.login_api.views import LoginDataView, GetPermissionsForUser
from frontend_utils.view_base import ViewBase, get_timezone_offset
from login.utils import InitAPI, APIError


LANGUAGES = (('fr', _('French')),
             ('de', _('German')),
             ('en', _('English')),
             ('ja', _('Japanese')),
             ('hi', _('Hindi')),)

tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__), "..", "tpls"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "configuration"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "nodes"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "jobs"),
                                         os.path.join(os.path.dirname(__file__), "..", "tpls", "error")],
                                         default_filters=['decode.utf8','h'],
                                         input_encoding='utf-8', output_encoding='utf-8')

log = logging.getLogger('iris')

class Login(ViewBase):
    """
    Handles login page related functionality. In get method it renders
    a login page and in post method it authenticate username and password.

    Attributes:
        template_name : string
                        Holds login.html as string and used in get and
                        post methods
        config_template_name: string
                        Holds configuration.mako as string and used in get and
                        post methods
    """
    template_name = 'login.html'
    config_template_name = 'configuration.mako'

    def get(self, request, *args, **kwargs):

        try:
            #rotate csrf token on login page
            rotate_token(request)
            if request.session['access_token']:
                if request.session['path_previous']:
                    return self.redirect(request.session['path_previous'])
                else:
                    return self.redirect('/dashboard/')
        except:
            # This localization feature has been done . The implementation of the same will be provided by Adaptive Team.
            # Currently we are hardcoding the session language to english
            request.session['django_language'] = 'en'
            return self.render_template(self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('uName', '')
        password = request.POST.get('pwd', '')
        username = username.strip()
        login_obj = LoginDataView()
        InitAPI_obj = InitAPI()
        
        timezone_local = request.POST.get('lDate')
        
        server_timezone = InitAPI_obj.get_server_timezone()
        timezone_offset = get_timezone_offset(timezone_local,server_timezone)

        login_response = login_obj.get(request, username, password)
        request.session['google_analytics'] = InitAPI_obj.getgoogleanalytics()
        try:
            if login_response.status_code == 200:
                request.session['username'] = username
                request.session['access_token'] = login_response.json()['access_token']
                request.session['token_type'] = login_response.json()['token_type']
                request.session['timezone_offset'] = timezone_offset
                request.session['expiry'] = login_response.json()['expires_in']
                # Setting session for BackDoorUser as NotBackDoorUser on successfully login
                request.session['BackDoorUser'] = 'NotBackDoorUser'
                # if user name is settings user name then permission api is not hit all permission is given to the user
                if str(username) == str(settings.USERNAME) and str(password) == str(settings.PASSWORD):
                    APIError.debug_log("Admin user moab-admin")
                    request.session['session_permission_list'] = settings.PERMISSIONS_LIST
                else:
                    permission_obj = GetPermissionsForUser()
                    permission_list, status = permission_obj.get(request)
                    if str(status) == '1':
                        APIError.debug_log("permissions " + ",".join(permission_list))
                        # checking if not 'Insight_user' and 'Insight_priv' in permission list
                        if 'read-insight-user' not in permission_list and 'read-insight-privileged' not in permission_list:
                            raw_message = "User {0} has no privileges."
                            APIError.debug_log(raw_message.format(username))
                            message = _(raw_message).format(username)
                            return self.render_template(self.template_name,
                                                        bad_string=message)
                        request.session['session_permission_list'] = permission_list
                    else:
                        request.session['session_permission_list'] = []

                request.session.set_expiry(request.session['expiry'])
                try:

                    request.session['path_previous']
                    return self.redirect(request.session['path_previous'])

                except:
                    return self.redirect('/dashboard/')
            else:
                if str(username) == str(InitAPI_obj.USERNAME) and str(password) == str(InitAPI_obj.PASSWORD):
                    # Setting session for BackDoorUser as NotBackDoorUser on unsuccessful login
                    request.session['BackDoorUser'] = 'BackDoorUser'
                    return self.redirect('/configuration/?backdoor=yes')
                else:
                    return self.render_template(self.template_name,
                                                bad_string=_('Please provide correct login credentials.'))
        except:
            if str(username) == str(InitAPI_obj.USERNAME) and str(password) == str(InitAPI_obj.PASSWORD):
                # Setting session for BackDoorUser as NotBackDoorUser on unsuccessful login
                request.session['BackDoorUser'] = 'BackDoorUser'
                return self.redirect('/configuration/?backdoor=yes')
            else:
                return self.redirect('/unauthorized/')
        else:
            return self.redirect('/login/')

class Logout(ViewBase):
    """
    Handles logout related functionality.

    Attributes:
            None
    """
    def get(self, request, *args, **kwargs):
        """
        Deletes session key if found in request.session() otherwise
        redirect to login page.

        Args:
            request: represents a single HTTP request. Request objects
                     also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect to login page, if any exception occures
            it redirects to login page.

        Raises:
            None
        """
        try:
            for sesskey in request.session.keys():
                del request.session[sesskey]

            return self.redirect('/login/')
        except:
            return self.redirect('/login/')
