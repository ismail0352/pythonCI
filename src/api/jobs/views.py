# coding=utf-8
"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import cgi
from datetime import timedelta, datetime
import json
import urllib

from django.utils import timezone
from django.utils.translation import ugettext
import re
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import WorkLoadSerializer, JobSummarySerializer, \
    SystemUtilizationSerializer, JobDetailSerializer, \
    JobMultiRequirementsSerializer, RequiredFeaturesSerializer
from login.utils import InitAPI, APIError


class WorkLoadDataView(InitAPI, APIView):
    """
    This class handles the workload grid data and the api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, query_set=None, format=None):
        """

        Build workload API url using payload which is form by api version and
        access token

        Workload API sample URL : http://www.sample.com/mws/rest/insight/priv/workload_view

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        query_set: string
                                                Use for multiple purpose
                                                query_set['sort'] : use to sort workload grid by column name
                                    query_set['max'],query_set['offset'] : use for pagination
                                                Default: None

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        Workload data ,success code and total count on success.
                        Error message, '0', error_status on failure.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            if query_set['query'] and query_set['sort']:
                query_string = '&max=' + str(query_set['max']) + '&offset=' + str(query_set['offset']) + '&sort=' + str(
                    query_set['sort']) + '&query={' + str('"$and":[') + str(query_set['query']) + ']}'

            elif query_set['sort']:
                query_string = '&max=' + str(query_set['max']) + '&offset=' + str(query_set['offset']) + '&sort=' + str(
                    query_set['sort'])
                # Keeping sort parameters in session for excel and xml generation
                request.session['sort_query'] = '&sort=' + str(query_set['sort'])

            elif query_set['jobStatus']:
                query_string = '&max=' + str(query_set['max']) + '&offset=' + str(query_set['offset']) + str(
                    query_set['offset']) + '&query={' + str('"$and":[') + str(query_set['jobStatus']) + ']}'

            elif query_set['query'] and query_set['offset']:
                query_string = '&max=' + str(query_set['max']) + '&offset=' + str(
                    query_set['offset']) + '&query={' + str('"$and":[') + str(query_set['query']) + ']}'

            elif query_set['query']:
                query_string = '&max=' + str(query_set['max']) + '&query={' + str('"$and":[') + str(
                    query_set['query']) + ']}'

            else:
                query_string = '&max=' + str(query_set['max']) + '&offset=' + str(
                    query_set['offset']) + '&sort={"job_sort":1}&sort={"job_id":1}'

            workLoadApi_url = self.baseUrl + "workload_view" + self.api_version + query_string
            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                workLoadApi_url = self.Server_baseUrl + 'rest/insight/user/' + "workload_view" + self.api_version + query_string

            workLoadApi_url = workLoadApi_url
            APIError.debug_log("workLoadApi_url " + workLoadApi_url)

            workload_data = requests.get(workLoadApi_url, headers=params)
            try:
                serializer = WorkLoadSerializer(data=workload_data.json()['results'], many=True)
                if serializer.is_valid():
                    data_workload = []
                    Total_Count = workload_data.json()["totalCount"]
                    for i in serializer.data:

                        dict = {}
                        FMT = '%Y-%m-%d %H:%M:%S'
                        if i['wallclock_seconds'] == None:
                            i['wallclock_seconds'] = 0

                        if i['wallclock_seconds']:
                            wallclock_sec = i['wallclock_seconds']
                            sec = timedelta(seconds=int(wallclock_sec))
                            d = datetime(1, 1, 1) + sec
                            days = int(wallclock_sec) / 86400
                            days = re.sub("\.\d+", "", str(days))
                            if int(days) < 10:
                                days = "0" + str(days)
                            hours = d.hour
                            if int(hours) < 10:
                                hours = "0" + str(hours)
                            minutes = d.minute
                            if int(minutes) < 10:
                                minutes = "0" + str(minutes)

                            seconds = d.second
                            if int(seconds) < 10:
                                seconds = "0" + str(seconds)
                            duration_format_wallclock = str(days) + ":" + str(hours) + ":" + str(minutes) + ":" + str(
                                seconds)
                        else:
                            duration_format_wallclock = "00:00:00:00"

                        # Elapsed Time calculated depending on the states of jobs.If state is completed , elapsed time is the difference between the current time and the job start time.
                        if i['job_state'] in ("RUNNING", "STAGING", "STARTING"):
                            if i['job_start_datetime']:
                                tdelta = datetime.strptime(re.sub("\.\d*.*$", "", str(timezone.now())),
                                                           FMT) - datetime.strptime(
                                    re.sub("\ \w*$", "", str(i['job_start_datetime'])), FMT)
                                sec = timedelta(seconds=int(tdelta.seconds))
                                elapsed = datetime(1, 1, 1) + sec
                                days = tdelta.days
                                if int(days) < 10:
                                    days = "0" + str(days)
                                hours = elapsed.hour
                                if int(hours) < 10:
                                    hours = "0" + str(hours)
                                minutes = elapsed.minute
                                if int(minutes) < 10:
                                    minutes = "0" + str(minutes)
                                seconds = elapsed.second
                                if int(seconds) < 10:
                                    seconds = "0" + str(seconds)
                                duration_format_elapsed = str(days) + ":" + str(hours) + ":" + str(minutes) + ":" + str(
                                    seconds)
                                elapsed_time_string = "elapsed time :" + str(duration_format_elapsed)
                            else:
                                elapsed_time_string = 'elapsed time : -'

                        elif i['job_state'] in ("COMPLETED", "FAILED", "REMOVED", "VACATED"):
                            if i['job_start_datetime'] and i['completion_datetime']:
                                tdelta = datetime.strptime(re.sub("\ \w*$", "", str(i['completion_datetime'])),
                                                           FMT) - datetime.strptime(
                                    re.sub("\ \w*$", "", str(i['job_start_datetime'])), FMT)
                                sec = timedelta(seconds=int(tdelta.seconds))
                                elapsed = datetime(1, 1, 1) + sec
                                days = tdelta.days
                                if int(days) < 10:
                                    days = "0" + str(days)
                                hours = elapsed.hour
                                if int(hours) < 10:
                                    hours = "0" + str(hours)
                                minutes = elapsed.minute
                                if int(minutes) < 10:
                                    minutes = "0" + str(minutes)
                                seconds = elapsed.second
                                if int(seconds) < 10:
                                    seconds = "0" + str(seconds)
                                duration_format_elapsed = str(days) + ":" + str(hours) + ":" + str(minutes) + ":" + str(
                                    seconds)
                                elapsed_time_string = "elapsed time :" + str(duration_format_elapsed)
                            else:
                                elapsed_time_string = 'elapsed time : -'

                        else:
                            elapsed_time_string = 'elapsed time : -'

                        dict["job_id"] = i['job_name']
                        dict["user_name"] = i['user_name']
                        dict["priority"] = i['priority']
                        dict["job_state"] = i['job_state']
                        dict["job_start_datetime"] = i['job_start_datetime']
                        # Commenting code to remove rank columns --IRIS-309
                        #dict["rank"] = i['rank']
                        dict["elapsed_time"] = elapsed_time_string
                        if i['resources']:
                            dict["resources"] = len(i['resources'].split(','))
                        else:
                            dict["resources"] = '-'
                        dict["wallclock_seconds"] = duration_format_wallclock
                        dict["utilization"] = ""
                        dict["uChartjobId"] = i['job_id']
                        dict["processor_count"] = i['processor_count']
                        dict["node_count"] = i['node_count']

                        data_workload.append(dict)
                    # success status for valid responces from api
                    success_status = 2000
                    return data_workload, Total_Count, success_status
                else:
                    # error status for no responses from api and exception
                    error_status = -1
                    error_message = ugettext('Exception During data proccessing..')
                    return error_message, 0, error_status
            except:
                # error status for invalid responses from api
                error_status = -1
                error_message = str("".join(workload_data.json()['messages']))
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


class JobSummaryDataView(InitAPI, APIView):
    """
    This class handles the job summary graph and the api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, format=None):
        """

        Build job summary API url using payload which is form by api version and
        access token

        job summary API sample URL : http://www.sample.com/mws/rest/insight/priv/job_summary_view

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        Job summary data on success.
                        Error message on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            jobSummaryApi_url = self.baseUrl + "job_summary_view" + self.api_version

            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                jobSummaryApi_url = self.Server_baseUrl + 'rest/insight/user/' + "job_summary_per_user_view" + self.api_version

            APIError.debug_log("jobSummaryApi_url " + jobSummaryApi_url)

            jobsummary_data = requests.get(jobSummaryApi_url, headers=params)
            try:

                serializer = JobSummarySerializer(data=jobsummary_data.json()['results'], many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
            except:
                return Response(jobsummary_data.json())

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


class SystemUtilizationDataView(InitAPI, APIView):
    """
    This class handles the System Utilization graph and the api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, format=None):
        """

        Build system utilization API url using payload which is form by api version and
        access token

        system utilization API sample URL : http://www.sample.com/mws/rest/insight/priv/system_dedication_and_utilization_view

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        system utilization data on success.
                        Error message on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}
            # string to append after the api gets appended with the actual timins (It is in Asia TimeZone.)
            #we have calculated one hour before the server time and appending it to the string
            required_time = re.sub("\W\d{3,}\W\d{2,}\W\d{2,}", "",
                                   str(timezone.localtime(timezone.now()) - timedelta(days=1)))
            string_append = 'system_dedication_interval_hours_view' + self.api_version + '&sort={%22timestamp_datetime%22:1}&pretty=true&query={"$and":[{"timestamp_datetime":{"$gte":"' + str(
                required_time) + ' UTC"}}]}'

            systemUtilizationApi_url = self.baseUrl + string_append

            APIError.debug_log("systemUtilizationApi_url " + systemUtilizationApi_url)
            systemutilization_data = requests.get(systemUtilizationApi_url, headers=params)

            try:
                serializer = SystemUtilizationSerializer(data=systemutilization_data.json()['results'], many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
            except:
                return Response(systemutilization_data.json())

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


# Commenting code for Utilization Charts --IRIS-293
'''
class UtilizationDataView(InitAPI,APIView):
    """
        This class handles the Utilization graph and the api call

        It inherits InitAPI class and  initialise some important variables like CLIENTID,
        CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.
    """

        def get(self, request, format=None):
            """
                Build utilization API url using payload which is form by api version and
                access token

                utilization API sample URL : http://www.sample.com/mws/rest/insight/priv/job_samples_view

                Args:
                        request: represents a single HTTP request. Request objects also have
                                         a few useful methods like GET,POST,DELETE,SESSION etc.

                                                   format: string
                                                           Grabs format string
                                                           Default: None

                Returns:
                                                utilization graph data on success.
                                                Error message on failure.('Exception During data proccessing')

                Raises:
                                                API connection exception.
                                                KeyError if access token not found.
            """

                try:
                                token_string = request.session['token_type'] + request.session['access_token']
                                params = {'Authorization':token_string}

                                job_id = request.GET.get("jobId")

                                jobSamplesApi_url = self.baseUrl + "job_samples_view" + self.api_version + "&query=%7Bjob_id:" + str(job_id) +"%7D&fields=timestamp_datetime,processor_utilization_percentage&sort={timestamp_datetime:1}"
                                if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                                                jobSamplesApi_url = self.URL+ '/mws/rest/insight/user/'+ "job_samples_view" + self.api_version + "query=%7Bjob_id:" + str(job_id) +"%7D&fields=timestamp_datetime,processor_utilization_percentage&sort={timestamp_datetime:1}"

                                APIError.debug_log("jobSamplesApi_url "+jobSamplesApi_url)
                                utilization_data = requests.get(jobSamplesApi_url , headers=params)
                                # Serialization job_samples_view for Utilization data and graph
                                try:
                                                serializer = UtilizationSerializer(data = utilization_data.json()['results'], many=True)
                                                if serializer.is_valid():
                                                                utilization_list=[]
                                                                utilization_graph = [["timestamp_datetime", "processor_utilization_percentage"]]
                                                                for j in serializer.data:
                                                                                utilization_list.append(j['processor_utilization_percentage'])
                                                                                # Taking Time stamp using slicing
                                                                                timestamp_datetime = j['timestamp_datetime']
                                                                                timestamp = str(timestamp_datetime[11:19])

                                                                                # Adjusting Decimal for processor_utilization_percentage
                                                                                processor_utilization_percentage = int(math.floor(j['processor_utilization_percentage']))

                                                                                utilization_graph.append([ timestamp, processor_utilization_percentage])

                                                                # Manipulation for maximum & minimum utilisation ranges
                                                                min_ut_range = int(math.floor(min(utilization_list)))
                                                                max_ut_range = int(math.ceil(max(utilization_list)))

                                                                utilization_range = str(min_ut_range)+"-"+str(max_ut_range)+"%"
                                                                utilization_graph_data = [ [utilization_range] , utilization_graph]
                                                                return Response(utilization_graph_data)
                                except:
                                                return Response(serializer.errors)

                                else:
                                                # error status for no responses from api and exception
                                                error_message = {}
                                                error_message['messages'] = 'Exception During data proccessing'
                                                return Response(error_message)

                except requests.exceptions.ConnectionError as e:
                                #Redirecting to error Page
                                return Response(APIError.error_log(e))

                except KeyError as key:
                                #Redirecting to error Page
                                return Response(APIError.error_log(key))

                except Exception as eX:
                                #Redirecting to error Page
                                return Response(APIError.error_log(eX))
'''

class GenerateReportsDataView(InitAPI, APIView):
    """
    This class handles the Report generation and the api call

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, query_set=None, format=None):
        """

        Build workoad API url using payload which is form by api version and
        access token

        workoad API sample URL : http://www.sample.com/mws/rest/insight/priv/workload_view

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        workload data on success.
                        Error message on failure.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """
        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            if "sort_query" in request.session:
                # Generating report based on the user sort on any column in the table
                workLoadApi_url = self.baseUrl + "workload_view" + self.api_version + str(request.session['sort_query'])
            else:
                # Default sort will be on troubled jobs for Generating Excel or XML
                workLoadApi_url = self.baseUrl + "workload_view" + self.api_version + '&sort={"job_sort":1}&sort={"job_id":1}'

            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in \
                    request.session['session_permission_list']:

                if "sort_query" in request.session:
                    # Generating report based on the user sort on any column in the table
                    workLoadApi_url = self.Server_baseUrl + 'rest/insight/user/' + "workload_view" + self.api_version + str(request.session['sort_query'])
                else:
                    # Default sort will be on troubled jobs for Generating Excel or XML
                    workLoadApi_url = self.Server_baseUrl + 'rest/insight/user/' + "workload_view" + self.api_version + '&sort={"job_sort":1}&sort={"job_id":1}'

            APIError.debug_log("workLoadApi_url " + workLoadApi_url)
            workload_data = requests.get(workLoadApi_url, headers=params)
            try:
                serializer = WorkLoadSerializer(data=workload_data.json()['results'], many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
            except:
                error_message = str("".join(workload_data.json()['messages']))
                return error_message
            else:
                error_message = "Exception while Processing"
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


class ModifyJobsStatusView(InitAPI, APIView):
    """
    This class handles the modifying job status

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, jobId=None, changeStatus=None, format=None):
        """

        Build job modify  API url using payload which is form by api version and
        access token

        job modify API sample URL : http://www.sample.com/mws/rest/jobs/nativerm.36?api-version=3&access_token=17462ac2-1325-49e4-862c-caf0b1f37d88&change-mode=set

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                           jobId: string
                               Grabs jonid string
                               Default: None

        changeStatus: string
                               Grabs changeStatus string
                               Default: None

                           format: string
                               Grabs format string
                               Default: None

        Returns:
                        Response message on success.
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

            jobmodifyApi_url = self.baseUrl_jobModify + str(jobId) + '/' + str(changeStatus) + self.api_version
            APIError.debug_log("jobmodifyApi_url " + jobmodifyApi_url)

            if str(changeStatus) == 'hold':
                # Request bodies are required for holding or unholding jobs
                json_body = {"holds": ["User"]}

                jobStatus_data = requests.put(jobmodifyApi_url, data=json.dumps(json_body), headers=params)

            else:
                jobStatus_data = requests.put(jobmodifyApi_url, headers=params)

            try:
                if jobStatus_data.status_code in (200, 201):
                    status = "success"
                    response_message = "".join(str(jobStatus_data.json()['messages'][0]))
                    return response_message, status
                else:
                    response_message = "".join(str(jobStatus_data.json()['messages'][0]))
                    return response_message, status
            except Exception as eX:
                APIError.debug_log(eX)
                return "Request is undefined", status

        except requests.exceptions.ConnectionError as e:
            # Redirecting to error Page
            return APIError.error_log(e), status

        except KeyError as key:
            # Redirecting to error Page
            return APIError.error_log(key), status

        except Exception as eX:
            # Redirecting to error Page
            return APIError.error_log(eX), status


class JobDetailsGetDataView(InitAPI, APIView):
    """
    This class handles the Job details api calls

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, job_name=None, format=None):
        """

        Build job details API url using payload which is form by api version and
        access token

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
                        jobdetails_data on success code.
                        Error message, '0', error_status on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            if job_name:
                string_append = 'job_details_view' + self.api_version + '&query={"name":"' + str(job_name) + '"}'

            jobDetailsApi_url = self.baseUrl + string_append

            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                jobDetailsApi_url = self.Server_baseUrl  + 'rest/insight/user/' + string_append

            APIError.debug_log("jobDetailsApi_url " + jobDetailsApi_url)
            jobdetails_data = requests.get(jobDetailsApi_url, headers=params)

            try:
                serializer = JobDetailSerializer(data=jobdetails_data.json()['results'], many=True)
                if serializer.is_valid():
                    # success status for valid responces from api
                    success_status = 2000
                    return serializer.data, success_status
            except:
                # error status for invalid responses from api
                error_status = -1
                error_message = str("".join(jobdetails_data.json()['messages']))
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


class JobDetailsMultiReqDataView(InitAPI, APIView):
    """
    This class handles the Job requirements api calls

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, job_name):
        """

        Build job requirements API url using payload which is form by api version and
        access token

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE,SESSION etc.

                        job_name: string
                               Grabs node_name string
                               Default: None
        Returns:
                        jobrequirements_data with success code.
                        Error message, '0', error_status on failure.('Exception During data proccessing')

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            if job_name:
                string_append = 'job_requirements_view' + self.api_version + '&query={"name":"' + str(job_name) + '"}'
            else:
                error_status = -1
                error_message = "Exception During data proccessing'"
                return error_message, error_status

            jobDetailsApi_url = self.baseUrl + string_append

            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                jobDetailsApi_url = self.Server_baseUrl + 'rest/insight/user/' + string_append

            APIError.debug_log("jobDetailsApi_url " + jobDetailsApi_url)
            jobrequirements_data = requests.get(jobDetailsApi_url, headers=params)
            try:
                serializer = JobMultiRequirementsSerializer(data=jobrequirements_data.json()['results'], many=True)
                if serializer.is_valid():
                    # success status for valid responces from api
                    success_status = 200
                    return serializer.data, success_status
            except:
                # error status for invalid responses from api
                error_status = -1
                error_message = "error"
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


class JobDetailsPostDataView(InitAPI, APIView):
    """
    This class handles the Job details api calls to modify jobs"

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    """

    def get(self, request, job_name, job_change_json):
        """
        Modify job status

        Args:
            request: represents a single HTTP request

            job_name: string, name of job

            job_change_json: Dictionary, changes to make to the job

        Returns: (message, status)
            message is string to display to user
            status is string "fail" on error, integer 200 on success

        """
        status = "fail"
        if not job_change_json:
            status = 200
            return "No modifications made", status

        token_string = request.session['token_type'] + request.session['access_token']
        params = {'Authorization': token_string}
        params = dict(params.items() + self.headers.items())

        job_modify_url = (self.baseUrl_jobModify +
                          urllib.quote(job_name, safe='') +
                          self.api_version + self.changemodeset)
        APIError.debug_log("job_modify_url " + job_modify_url)
        # Passing simple put request using creds as token is not working

        try:
            job_modify_response = requests.put(job_modify_url,
                                               data=json.dumps(job_change_json),
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
            response_json = job_modify_response.json()
        except Exception as e:
            message = "Server did not return valid JSON: {0}".format(e)
            APIError.error_log(message)
            return (message, status)
        messages_json = response_json['messages']
        # Messages from MWS could contain anything, including JavaScript
        # Since the Mako template won't escape messages, we need to here.
        messages = [cgi.escape(m, quote=True) for m in messages_json]

        if job_modify_response.status_code in (200, 201):
            # No error
            messages.append(
                "The job has been successfully updated. "
                "Changes will be reflected after the next scheduling iteration.")
            status = 200
        return "<br/>".join(messages), status


class RequiredFeaturesDataView(InitAPI, APIView):
    """
    This class handles api calls for Required Features in Job details page

    It inherits InitAPI class and  initialise some important variables like CLIENTID,
    CLIENTSECRET, GOOGLE_ANALYTICS,baseUrl, baseUrl_configfeaturesModify, baseUrl_permission etc.

    Get required features using job name

    """

    def get(self, request, job_name=None, format=None):
        """

        Get required features

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
                        requiredfeatures_data on success code.

        Raises:
                        API connection exception.
                        KeyError if access token not found.

        """

        try:
            token_string = request.session['token_type'] + request.session['access_token']
            params = {'Authorization': token_string}

            features_query = "node_feature_view" + self.api_version
            required_featureApi_url = self.baseUrl + features_query
            
            if 'read-insight-user' in request.session['session_permission_list'] and 'Job View All' not in request.session['session_permission_list']:
                required_featureApi_url = self.Server_baseUrl + 'rest/insight/user/' + features_query

            APIError.debug_log("required_featureApi_url " + required_featureApi_url)
            requiredfeatures_data = requests.get(required_featureApi_url, headers=params)
            try:
                serializer = RequiredFeaturesSerializer(data=requiredfeatures_data.json()['results'], many=True)
                if serializer.is_valid():
                    return serializer.data
            except:
                error_message = str("".join(requiredfeatures_data.json()['messages']))
                return error_message

        except requests.exceptions.ConnectionError as e:
            return Response(APIError.error_log(e))

        except KeyError as key:
            return Response(APIError.error_log(key))

        except Exception as eX:
            return Response(APIError.error_log(eX))


