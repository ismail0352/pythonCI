# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import cgi
import json
import urllib
from django.utils.translation import ugettext
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ResourceSummarySerializer, ResourceListSerializer, \
    NodeDetailsSerializer, GenericResourcesSerializer, \
    ConfigurableFeaturesSerializer, GenericResourcesPerNodeSerializer
from login.utils import InitAPI, APIError


class ResourceSummaryDataView(InitAPI, APIView):
    """
    This class handles the Resource Summary graph and the api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, format=None):
        """

        Build resource summary API url using payload which is form by api version and
        access token

        resource summary API sample URL : http://www.sample.com/mws/rest/nodes
                                                                          /node005?api-version=3&access_token=17462ac2-1325-49e4-862c-caf0b1f37d88&change-mode=set

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        resource summary data on success.
                        Error message on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            resourceSummaryApi_url = self.baseUrl + "node_summary_view" + self.api_version

            APIError.debug_log("resourceSummaryApi_url " + resourceSummaryApi_url)
            resourcesummary_data = requests.get(resourceSummaryApi_url, headers=params)
            try:
                serializer = ResourceSummarySerializer(data=resourcesummary_data.json()['results'], many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
            except:
                return Response(resourcesummary_data.json())

            else:
                # error status for no responses from api and exception
                error_message = {}
                error_message['messages'] = 'Exception During data proccessing'
                return Response(error_message)

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

class ResourceListDataView(InitAPI, APIView):
    """
    This class handles the Resource List api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, query_set=None, format=None):
        """

        Build resource list API url using payload which is form by api version and
        access token

        resource list API sample URL : http://www.sample.com/mws/rest/roles

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        query_set: string
                                                Use for multiple purpose
                                                query_set['sort'] : use to sort resource list by column name
                                    query_set['max'],query_set['offset'] : use for pagination
                                                Default: None

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        resourcelist data ,success code and total count on success.
                        Error message, '0', error_status on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                KeyError if access token not found.

        """

        try:
            # Commenting code for -IRIS-451
            # if 'read-insight-priv' not in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
            #    return [],0,200

            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            if query_set:
                if query_set['sort'] and query_set['query']:
                    query_string = '&max=' + str(query_set['max']) + '&offset=' + str(
                        query_set['offset']) + '&sort=' + str(query_set['sort']) + '&query={' + str('"$and":[') + str(
                        query_set['query']) + ']}'

                elif query_set['sort']:
                    query_string = '&max=' + str(query_set['max']) + '&offset=' + str(
                        query_set['offset']) + '&sort=' + str(query_set['sort'])

                elif query_set['jobStatus']:
                    query_string = "&pretty=true&" + 'max=' + str(query_set['max']) + '&offset=' + str(
                        query_set['offset']) + '&query={' + str('"$and":[') + str(query_set['jobStatus']) + ']}'

                elif query_set['query'] and query_set['offset']:
                    query_string = '&max=' + str(query_set['max']) + '&offset=' + str(
                        query_set['offset']) + '&query={' + str('"$and":[') + str(query_set['query']) + ']}'

                elif query_set['query']:
                    query_string = '&max=' + str(query_set['max']) + '&query={' + str('"$and":[') + str(
                        query_set['query']) + ']}'

                else:
                    query_string = '&max=' + str(query_set['max']) + '&offset=' + str(query_set['offset'])

            else:
                query_string = ""

            resourceListApi_url = self.baseUrl + "node_management_view" + self.api_version + query_string

            # Adding code for -IRIS-451
            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                resourceListApi_url = self.Server_baseUrl + 'rest/insight/user/' + "node_management_view" + self.api_version + query_string

            APIError.debug_log("resourceListApi_url " + resourceListApi_url)

            resourcelist_data = requests.get(resourceListApi_url, headers=params)
            try:
                serializer = ResourceListSerializer(data=resourcelist_data.json()['results'], many=True)

                if serializer.is_valid():
                    success_status = 200
                    return serializer.data, resourcelist_data.json()["totalCount"], success_status
            except:
                # error status for invalid responses from api
                error_status = -1
                error_message = str("".join(resourcelist_data.json()['messages']))
                if resourcelist_data.status_code == 400:
                    error_message = ugettext('Only administrators may view node and job features.')
                return error_message, 0, error_status
            else:
                # error status for no responses from api and exception
                error_status = -1
                error_message = 'Exception During data proccessing'
                return error_message, 0, error_status

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

class NodeDetailsDataView(InitAPI, APIView):
    """
    This class handles the Node details api calls

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    shows node details using node name

    """

    def get(self, request, node_name=None, format=None):

        """
        Build node details API url using payload which is form by api version and
        access token

        node detail API sample URL : http://www.sample.com/mws/rest/insight/priv/node_details_view

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        node_name: string
                               Grabs node_name string
                               Default: None

                           format: string
                               Grabs format string
                               Default: None
        Returns:
                        node detail data on success code.
                        Error message, '0', error_status on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            node_query = "node_details_view" + str(self.api_version) + '&query={"name":"' + str(node_name) + '"}'

            nodeDetailsApi_url = self.baseUrl + node_query
            APIError.debug_log("nodeDetailsApi_url " + nodeDetailsApi_url)
            nodedetails_data = requests.get(nodeDetailsApi_url, headers=params)
            try:
                serializer = NodeDetailsSerializer(data=nodedetails_data.json()['results'], many=True)
                if serializer.is_valid():
                    # success status for valid responces from api
                    success_status = 2000
                    return serializer.data, success_status
            except:
                # error status for invalid responses from api
                error_status = -1
                error_message = "".join(str(nodedetails_data.json()['messages']))
                return error_message, error_status

            else:
                # error status for no responses from api and exception
                error_status = -1
                error_message = 'Exception During data proccessing'
                return error_message, error_status

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return Response(APIError.error_log(e))

        except KeyError as key:
            # Redirecting to error Page
            return Response(APIError.error_log(key))

        except Exception as eX:
            # Redirecting to error Page
            return Response(APIError.error_log(eX))

    def post(self, request, node_name, node_change_json):
        """
        Node detail edit

        Args:
            request: represents a single HTTP request

            node_name: string, name of node to modify

            node_change_json: Dictionary, changes to make to node

        Returns: (message, status)
            message is string to display to user
            status is string "fail" on error, "success" on success
        """
        status = "fail"
        if not node_change_json:
                status = "success"
                return "No modifications made.", status
        token_string = request.session['token_type'] + request.session['access_token']
        params = {'Authorization': token_string}
        params = dict(params.items() + self.headers.items())

        node_modify_url = (self.baseUrl_configfeaturesModify +
                           urllib.quote(node_name, safe='') +
                           self.api_version + self.changemodeset)
        APIError.debug_log("node_modify_url " + node_modify_url)

        try:
            node_modify_response = requests.put(node_modify_url,
                                                data=json.dumps(node_change_json),
                                                headers=params)
        except requests.exceptions.ConnectionError as e:
            message = "Error connecting to MWS server: {0}".format(e)
            APIError.error_log(message)
            return message, status
        except Exception as e:
            message = "Error communicating with MWS server: {0}".format(e)
            APIError.error_log(message)
            return message, status
        # job_modify_response.json()['messages'] is a list of unicode
        # strings, each containing a message to display.
        try:
            response_json = node_modify_response.json()
        except Exception as e:
            message = "Server did not return valid JSON: {0}".format(e)
            APIError.error_log(message)
            return (message, status)
        messages_json = response_json['messages']
        # Messages from MWS could contain anything, including JavaScript
        # Since the Mako template won't escape messages, we need to here.
        messages = [cgi.escape(m, quote=True) for m in messages_json]

        if node_modify_response.status_code in (200, 201):
            # No error
            messages.append(
                "The node has been successfully updated. "
                "Changes will be reflected after the next scheduling iteration.")
            status = "success"
        return "<br/>".join(messages), status


class GenericResourceDataView(InitAPI, APIView):
    """
    This class handles api calls for Generic Resources in Job details page

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, job_name=None, format=None):
        """
        Get resource data

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        job_name: string
                               Grabs job_name string
                               Default: None

                           format: string
                               Grabs format string
                               Default: None
        Returns:
                        genericresources_data on success code.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            generic_query = "generic_resource_view" + self.api_version
            genericresourcesApi_url = self.baseUrl + generic_query
            APIError.debug_log("genericresourcesApi_url " + genericresourcesApi_url)
            genericresources_data = requests.get(genericresourcesApi_url, headers=params)
            try:
                serializer = GenericResourcesSerializer(data=genericresources_data.json()['results'], many=True)
                if serializer.is_valid():
                    return serializer.data
            except:
                Response(genericresources_data.json())

        except requests.exceptions.ConnectionError as e:
            return Response(APIError.error_log(e))

        except KeyError as key:
            return Response(APIError.error_log(key))

        except Exception as eX:
            return Response(APIError.error_log(eX))

class ConfigurableFeaturesDataView(InitAPI, APIView):
    """
    This class handles Configurable Features that is displayed in node details Page

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, job_name=None, format=None):
        """
        Modify principal

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

              job_name: string
                                         Grabs job_name string
                                         Default: None

                 format: string
                                         Grabs format sting
                                         Default: None
        Returns:
                        configurablefeatures_data  on success.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            configurable_features_query = "user_interface_node_feature_view" + self.api_version
            configurableFeaturesApi_url = self.baseUrl + configurable_features_query
            APIError.debug_log("configurableFeaturesApi_url " + configurableFeaturesApi_url)
            configurablefeatures_data = requests.get(configurableFeaturesApi_url, headers=params)
            try:
                serializer = ConfigurableFeaturesSerializer(data=configurablefeatures_data.json()['results'], many=True)
                if serializer.is_valid():
                    return serializer.data
            except:
                Response(configurablefeatures_data.json())

        except requests.exceptions.ConnectionError as e:
            return APIError.redirect_error_page(e)

        except KeyError as key:
            return APIError.redirect_error_page(key)

        except Exception as eX:
            return APIError.redirect_error_page(eX)

class GenericResourcePerNodeDataView(InitAPI, APIView):
    """
    This class handles api calls for Generic Resources Per Node in Node details page

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, node_name=None, format=None):
        """
        Get resource data

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        job_name: string
                               Grabs node_name string
                               Default: None

                           format: string
                               Grabs format string
                               Default: None
        Returns:
                        genericresourcespernode_data on success code.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            # Need to modify the url once it is updated in ngui-cybage2.ac
            genericresourcespernode_query = "generic_resources_per_node_view" + self.api_version + '&query={"node_name":"' + str(
                node_name) + '"}&sort={"generic_resource":1}'
            genericresourcespernodeApi_url = self.baseUrl + genericresourcespernode_query

            APIError.debug_log("genericresourcespernodeApi_url " + genericresourcespernodeApi_url)

            genericresourcespernode_data = requests.get(genericresourcespernodeApi_url, headers=params)

            try:
                serializer = GenericResourcesPerNodeSerializer(data=genericresourcespernode_data.json()['results'],
                                                               many=True)
                if serializer.is_valid():
                    return serializer.data
            except:
                Response(genericresourcespernode_data.json())

        except requests.exceptions.ConnectionError as e:
            return Response(APIError.error_log(e))

        except KeyError as key:
            return Response(APIError.error_log(key))

        except Exception as eX:
            return Response(APIError.error_log(eX))

