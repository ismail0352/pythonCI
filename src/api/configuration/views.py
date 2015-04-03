# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

import json
import socket
import sys

from django.conf import settings
from django.utils.translation import ugettext
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import simplejson
import urllib3

from api.installation import Installation_settings
from login.utils import InitAPI, APIError


class ConfigurationDataView(InitAPI, APIView):
    """
    Read Write config file

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request):
        """
        Configuration data

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        filedata(USERNAME, PASSWORD, CLIENTID, CLIENTSECRET etc.)

        Raises:
                        None

        """
        try:
            filedata = {}
            filedata['USERNAME'] = self.USERNAME
            filedata['PASSWORD'] = self.PASSWORD
            filedata['CLIENTID'] = self.CLIENTID
            filedata['CLIENTSECRET'] = self.CLIENTSECRET
            filedata['URL'] = self.URL
            filedata['SUB_URL'] = self.SUB_URL
            filedata['GOOGLE_ANALYTICS'] = self.GOOGLE_ANALYTICS
            filedata['SERVER_TIMEZONE'] = self.SERVER_TIMEZONE

        except Exception as eX:
            return Response(APIError.error_log(eX))

        return filedata

    def post(self, request, filedata):
        """
        Modify or new Configuration data

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        filedata: Dictionary
                                          Containing USERNAME, PASSWORD, CLIENTID, CLIENTSECRET etc.

        Returns:
                        'Success' string if file opreation goes right else
                        'Fail'

        Raises:
                        None

        """
        try:
            url = filedata["URL"]
            username = filedata["USERNAME"]
            passwd = filedata["PASSWORD"]
            clientid = filedata["CLIENTID"]
            clientsecret = filedata["CLIENTSECRET"]
            sub_url = filedata["SUB_URL"]

            # first check if MWS is good before checking if oauth is enabled
            if requests.post(url + sub_url,
                             timeout=settings.CONNECTION_TIMEOUT).status_code == requests.codes.not_found:
                APIError.debug_log("MWS validation error: MWS server or path not found")
                # Fail due to invalid path or Path not found
                return "Exception", ugettext("Either MWS is not running or the Path is wrong")

            # Check on provided credentials is valid or not using login api call
            params = {'grant_type' : "password",'username' : username,'password' : passwd,
                      'client_id' : clientid, 'client_secret' : clientsecret }
            
            ConfigCheckApi_url = url + sub_url + "oauth/token"
            
            APIError.debug_log("ConfigCheckApi_url " + ConfigCheckApi_url)
            configtest_response = requests.post(ConfigCheckApi_url, data=params,  timeout=settings.CONNECTION_TIMEOUT)
    
            if configtest_response.status_code == 200 and configtest_response.content is not None:
                token_string = configtest_response.json()["token_type"] + configtest_response.json()["access_token"]
                params = {"Authorization":token_string}
                try:
                    del request.session['access_token']
                    request.session['access_token'] = configtest_response.json()['access_token']
                except:
                    request.session['access_token'] = configtest_response.json()['access_token']
    
                # Checking the action test and return success without saving data
                if str(filedata['ACTION']) == 'test':
                    return "TestSuccess"
                
                with open(settings.CONFIG_PATH, "w", 0) as json_data:
                    json_data.write(json.dumps(filedata, indent=4))
                    json_data.flush()
                    json_data.close()
                    APIError.debug_log("Success written in config file")
        
                    # Check Reset Permissions status if checked set permissions
                    setpermissions_status = request.POST.get("resetpermission")
                    if str(setpermissions_status) == '1':
                        APIError.debug_log("Resetting all the permissions and roles")
                        APIobj = InitAPI()
                        install_Obj = Installation_settings(APIobj, params)
                        res = install_Obj.IRISPermissions()
                        del APIobj, install_Obj
                        if res == "Success":
                            return "Success"
                        elif res[0] == "Fail":
                            return "Fail", res[1]
                        else:
                            return "Exception", res[1]
                            
                # Successfully modified all parameters on configuration page
                return "Success"
            
            elif configtest_response.status_code == requests.codes.not_found:
                APIError.debug_log("Failed to authenticate. OAuth is not not setup or this MWS is an older version.")
                # Fail due to invalid path or Path not found
                error_message = ugettext("Unsupported MWS version")
            else:
                if 'messages' in configtest_response.json():
                    # Fail due to invalid username or password
                    error_message = ", ".join(configtest_response.json()['messages'])
                elif 'error_description' in configtest_response.json():
                    # Fail due to invalid clientid or client secret
                    error_message = ugettext("Error authenticating with OAuth: {0}").format("".join(str(configtest_response.json()['error_description'])))
                else:
                    # Fail due to no response content
                    error_message = ugettext("No response content: {0}").format(configtest_response.reason)

        except requests.ConnectionError as eX:
            if eX.message.reason.errno == socket.EAI_NONAME:
                error_message = ugettext("Invalid URL: No such host")
            else:
                error_message = ugettext("Connection error: {0}").format(eX.message.reason.strerror)
            APIError.debug_log(eX)
        except requests.exceptions.InvalidSchema as eX:
            # Fail due to invalid schema for url
            APIError.debug_log(eX)
            error_message = ugettext("Invalid URL: Unknown protocol (schema)")
        except requests.exceptions.MissingSchema as mSx:
            # Fail due to no protocol specified
            APIError.debug_log(mSx)
            error_message = ugettext("Invalid URL: No protocol (schema) supplied. Try http or https")
        except urllib3.exceptions.LocationParseError as eX:
            # Fail due to invalid syntax
            APIError.debug_log(eX)
            error_message = ugettext("Invalid URL: Syntax error")
            # return "Exception", error_message
        except simplejson.JSONDecodeError as jEx:
            # Fail due to invalid json
            APIError.debug_log(jEx)
            error_message = ugettext("Response contains invalid JSON. Server is probably not an MWS server.")
        except requests.Timeout as eX:
            APIError.debug_log(eX)
            error_message = ugettext("Read timed out. MWS Server is probably not responding.")
        except Exception as eX:
            # Fail due to general exception
            APIError.debug_log(eX)
            exception_type = sys.exc_info()[0]
            error_message = ugettext("Exception of type {0}: {1}").format(exception_type, eX)

        APIError.debug_log("MWS validation error: {0}".format(error_message))
        return "Exception", error_message

class RoleDataManagementView(InitAPI, APIView):
    """
    Getting Permission list

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request):
        """
        Get permission list according to access token

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        Permission list on success.

        Raises:
                        API connection error

        """
        try:

            """
            get permission list
            """
            permissionList = settings.PERMISSIONS_LIST
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            # get the permission data
            permurl = self.baseUrl_permission + self.api_version
            permurl = permurl.strip()
            APIError.debug_log("permurl " + permurl)
            permdata = requests.get(permurl, headers=params)

            permlist = []
            domainpermlist = []
            try:
                for i in permdata.json()['results']:
                    if i['label'] in permissionList:
                        if i['label'] not in ('read-insight-privileged', 'read-insight-user'):
                            permlist.append({i['id']: i})
                        else:
                            domainpermlist.append({i['id']: i})
                    else:
                        domainpermlist.append({i['id']: i})

                data = {}
                data['permissions'] = permlist
                data['domainpermissions'] = domainpermlist
                return data
            except:
                error_message = "".join(str(permdata.json()['messages'][0]))
                return error_message

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page

            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page

            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page

            return Response(APIError.error_log(eX))


class RoleModel(InitAPI, APIView):
    """
    Roles related opreations

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def createRole(self, request, roleid=None, roledict=None):
        """
        Create role opreaton

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                          roleid: integer
                              Default: None

                         roledict: dictionary
                               Grabs roledict dictionary
                               Default: None
        Returns:
                        response_message on success.
                        Error message on failure.('Request is undefined')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        status = "fail"
        try:

            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            params = dict(params.items() + self.headers.items())

            if roleid:
                roleurl = self.baseUrl_role + "/" + roleid + self.api_version + self.changemodeset
                roleurl = roleurl.strip()
                roleStatus_data = requests.put(roleurl, data=json.dumps(roledict), headers=params)


            else:
                roleurl = self.baseUrl_role + self.api_version + self.changemodeadd
                roleurl = roleurl.strip()
                roleStatus_data = requests.post(roleurl, data=json.dumps(roledict), headers=params)

            try:
                if roleStatus_data.status_code in (200, 201):
                    Onsuccessid = roleStatus_data.json()['id']
                    if roleid:
                        response_message = ugettext("Role {0} was updated Successfully").format(
                            roleStatus_data.json()['name'])
                    else:
                        response_message = ugettext("Role {0} was created Successfully").format(
                            roleStatus_data.json()['name'])
                    status = "success"
                    return response_message, Onsuccessid, status
                else:
                    roleStatus_data.json()['messages']
                    response_message = "".join(str(roleStatus_data.json()['messages'][0]))
                    return response_message, roleid, status
            except:
               return roleStatus_data.json()['messages'][0], roleid, status

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page

            return APIError.error_log(e), status

        except KeyError as key:
            # Redirecting to error Page

            return APIError.error_log(key), status

        except Exception as eX:
            # Redirecting to error Page

            return APIError.error_log(eX), status

    def getRole(self, request):
        """
        Returns role

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        roledata on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            roleid = request.GET.get("roleid")

            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            roleurl = self.baseUrl_role + "/" + roleid + self.api_version
            roleurl = roleurl.strip()

            roledata = requests.get(roleurl, headers=params)
            roledata = roledata.json()
            return roledata
        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def getRoleByName(self, request, name):
        """
        Returns role by name

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        name : string
                                   Grabs role name in name variable

        Returns:
                        roledata on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            if name:
                token_string = request.session['token_type'] + request.session['access_token']
                params = {'Authorization': token_string}

                roleurl = self.baseUrl_role + "/" + name + self.api_version
                roleurl = roleurl.strip()
                roledata = requests.get(roleurl, headers=params)
                roledata = roledata.json()
                return roledata
        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def getRoles(self, request):
        """
        Returns all roles

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        rolelist on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            # get all the roles
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            query_string = '&sort={"name":1}'

            roleurl = self.baseUrl_role + self.api_version + query_string
            roleurl = roleurl.strip()
            roledata = requests.get(roleurl, headers=params)
            rolelist = []
            try:
                for role in roledata.json()['results']:
                    rolelist.append({role['id']: role})
                status_code = 2000
                return rolelist, status_code
            except:
                status_code = 2001
                return roledata.json()['messages'][0], status_code

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def deleteRole(self, request):
        """
        Delete role

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        role url  on successful deletion of role.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            id = request.GET.get("id")
            roleurl = self.baseUrl_role + "/" + id + self.api_version
            response = requests.delete(roleurl, headers=params)
            return response.json()

        except requests.exceptions.ConnectionError as e:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(e))

        except KeyError as key:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(key))

        except Exception as eX:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(eX))


class PrincipalModel(InitAPI, APIView):
    """
    This Model class handles all api calls for principal listing edit create delete

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def getPrincipalListing(self, request):
        """
        Get principal list

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        principallist,totalcount on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            query_string = '&sort={"name":1}'
            principalurl = self.baseUrl_principal + self.api_version + query_string
            principalurl = principalurl.strip()

            APIError.debug_log("principalurl " + principalurl)

            principaldata = requests.get(principalurl, headers=params)
            try:
                totalcount = principaldata.json()["totalCount"]
                principallist = []
                for principal in principaldata.json()['results']:
                    principallist.append({principal['id']: principal})
                status_code = 2000
                return principallist, totalcount, status_code
            except:
                status_code = 2001
                totalcount = ''
                return principaldata.json()['messages'][0], totalcount, status_code

        except requests.exceptions.ConnectionError as e:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(e))

        except KeyError as key:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(key))

        except Exception as eX:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(eX))


    def deletePrincipal(self, request, principalid=None, principalname=None):
        """
        Delete principal

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                principalid: Integer
                                         Grabs principalid to delete principal
                                         Default: None

           principalname: string
                                         Grabs principalname to delete principal
                                         Default: None
        Returns:
                        principalStatus_data on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            principalDeletetApi_url = self.baseUrl_principal + principalid + self.api_version
            APIError.debug_log("principalDeletetApi_url " + principalDeletetApi_url)
            principalStatus_data = requests.delete(principalDeletetApi_url, headers=params)
            try:
                if principalStatus_data.status_code == 200:
                    # Commenting code for as we dont have message display for delete
                    #response_message = "principal  " + principalname + " has been deleted successfully"
                    return "Success"
                else:
                    principalStatus_data.json()['messages']
                    response_message = "".join(str(principalStatus_data.json()['messages'][0]))
                    return "Fail", response_message

            except Exception as eX:
                APIError.debug_log(eX)
                return "Exception", "Exception while Data Processing"

        except requests.exceptions.ConnectionError as e:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(e))

        except KeyError as key:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(key))

        except Exception as eX:
            # HERE WE ARE ADDING ERROR LOGGING
            return Response(APIError.error_log(eX))


    def getPrincipal(self, request, principalid=None, format=None):
        """
        Return single principal

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                principalid: Integer
                                         Grabs principalid to delete principal
                                         Default: None

                 format: string
                                         Grabs format sting
                                         Default: None
        Returns:
                        principal_data json format  on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            principalEditGetApi_url = self.baseUrl_principal + principalid + self.api_version
            APIError.debug_log("principalEditGetApi_url " + principalEditGetApi_url)
            principal_data = requests.get(principalEditGetApi_url, headers=params)

            try:
                if principal_data.status_code == 200:
                    name = principal_data.json()['name']
                    return "Success", principal_data.json()
                else:
                    principal_data.json()['messages']
                    response_message = "".join(str(principal_data.json()['messages'][0]))
                    return "Fail", response_message
            except:
                return principal_data.json()

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))
        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))
        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def getPrincipalByName(self, request, principalname=None, format=None):
        """
        Return single principal by name

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                principalname: string
                                         Grabs principalname to get principal
                                         Default: None

                 format: string
                                         Grabs format sting
                                         Default: None
        Returns:
                        principal_data json format  on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            principalEditGetApi_url = self.baseUrl_principal + principalname + self.api_version
            APIError.debug_log("principalEditGetApi_url " + principalEditGetApi_url)
            principal_data = requests.get(principalEditGetApi_url, headers=params)

            try:
                name = principal_data.json()['name']
                return principal_data.json()

            except:
                return principal_data.json()

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))
        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))
        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def post(self, request, principalid=None, principalname=None, modify_data=None, format=None):
        """
        Modify principal

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                principalid: Integer
                                         Grabs principalid Integer
                                         Default: None

           principalname: string
                                         Grabs principalname string
                                         Default: None

                     modify_data: dictionary
                                         Grabs modify_data to modify principal
                                         Default: None

                 format: string
                                         Grabs format sting
                                         Default: None
        Returns:
                        principal_data json format  on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        status = "fail"
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            params = dict(params.items() + self.headers.items())
            # currently fixing this for IRIS-418,386 need to configure this for every return messges

            if principalid:
                principalEditApi_url = self.baseUrl_principal + principalname + self.api_version + self.changemodeset
                principalStatus_data = requests.put(principalEditApi_url, data=json.dumps(modify_data), headers=params)

            else:
                principalCreateApi_url = self.baseUrl_principal + self.api_version + self.changemodeadd
                principalStatus_data = requests.post(principalCreateApi_url, data=json.dumps(modify_data),
                                                     headers=params)

            try:
                if principalStatus_data.status_code in (200, 201):
                    Onsuccessid = principalStatus_data.json()['id']
                    if principalid:
                        response_message = ugettext("Principal {0} was updated Successfully").format(
                            principalStatus_data.json()['name'])
                    else:
                        response_message = ugettext("Principal {0} was created Successfully").format(
                            principalStatus_data.json()['name'])
                    status = "success"
                    return response_message, Onsuccessid, status
                else:
                    response_message = "".join(str(principalStatus_data.json()['messages'][0]))
                    return response_message, principalid, status
            except:
                return principalStatus_data.json()['messages'][0], principalid, status

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return APIError.error_log(e), None, status

        except KeyError as key:
            # Redirecting to error Page
            return APIError.error_log(key), None, status

        except Exception as eX:
            # Redirecting to error Page
            return APIError.error_log(eX), None, status

    def getPrincipalEntity(self, request):
        """
        Returns principal entity

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

        Returns:
                        principalEntity_data(LDAP, PAM)  on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string, 'Content-type': 'application/json'}

            principalEntity_Api_url = self.baseUrl_principalEntity + self.api_version
            APIError.debug_log("principalEntity_Api_url " + principalEntity_Api_url)
            principalEntity_data = requests.get(principalEntity_Api_url, headers=params)
            try:
                # Getting LDAP PAM connection status from the health api
                LDAP = principalEntity_data.json()['ldap']['connected']
                PAM = principalEntity_data.json()['pam']['connected']
                # Adding lower case for values for LDAP and PAM 
                return str(LDAP).lower(), str(PAM).lower()
            except:
                # Set default FALSE for ENTITY in case you no request is from the api
                return "false", "false"

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))
        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))
        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))
