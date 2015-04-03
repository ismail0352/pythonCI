# coding=utf-8
"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

from django.conf import settings
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import LoginSerializer
from login.utils import InitAPI, APIError


class LoginDataView(InitAPI, APIView):
    """
    Handles login related functionality.

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, user_name=None, password=None, format=None):
        """
        Build login API url using payload which is form by username, password,
        clientid, clientsecret.

        login API sample URL : http://www.sample.com/mws/oauth/token

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

            user_name: string
                           Grabs username string
                           Default: None

             password: string
                           Grabs password string
                           Default: None

               format: string
                           Grabs format string
                           Default: None
        Returns:
                login_data, which is reponse of login API url if serializer is valid
                else returns string 'Config page'

        Raises:
            None

        """
        list_creds = []
        dict = {}
        dict["username"] = user_name
        dict["password"] = password

        client_id = self.CLIENTID
        client_secret = self.CLIENTSECRET

        list_creds.append(dict)
        serializer = LoginSerializer(data=list_creds, many=True)
        if serializer.is_valid():
            try:
                payload = "?grant_type=password" + "&username=" + user_name + "&password=" + password + "&client_id=" + client_id + "&client_secret=" + client_secret
                loginApi_url = self.baseUrl_login + payload
                login_data = requests.post(loginApi_url)
                return login_data
            except Exception as e:
                return "Config page"

        return Response(serializer.errors)


class GetPermissionsForUser(InitAPI, APIView):
    """
    This class handles the permission listing for all the logged user

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request):
        """

        Build permission API url using payload which is form by username, api version and
        access token

        Permission API sample URL : http://www.sample.com/mws/rest/permissions

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        Permission list with success code '1'.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            # Hitting permissions api for the logged in user
            permissionsApi_url = self.baseUrl_permission + "/users" + self.api_version
            APIError.debug_log("permissionsApi_url " + permissionsApi_url)

            try:
                permissions_data = requests.get(permissionsApi_url, headers=params)

                session_persmissions = []
                for permi in permissions_data.json()['permissions']:
                    if permi['label'] in settings.PERMISSIONS_LIST:
                        session_persmissions.append(str(permi['label']))
                return session_persmissions, 1

            except:
                return permissions_data.json(), 0

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

