# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import csv
from datetime import datetime, timedelta
import math
import re
import urllib
import xml.etree.ElementTree as ET

from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext

from api.jobs.views import WorkLoadDataView, JobDetailsGetDataView, \
    JobDetailsMultiReqDataView, RequiredFeaturesDataView, JobDetailsPostDataView, \
    GenerateReportsDataView, ModifyJobsStatusView
from api.nodes.views import ResourceListDataView
from frontend_utils.view_base import ViewBase, secured, local_2_utc, utc_2_local
from login.utils import APIError, WORKLOAD_FILTER_STATUS


class GetDashboardView(ViewBase):

    """
    Dashboard Page Rendering functionality

    Attributes:
        template_name : string
                        Holds dashboard.mako as string and used in get method

    """
    template_name = 'dashboard.mako'
    @secured
    def get(self, request, *args, **kwargs):

        if "session_permission_list" in request.session:
            if 'Workload' in request.session['session_permission_list']:
                message = ''
                storage = get_messages(request)
                for message in storage:
                    message = message
                request.session['active_tab'] = "dashboard"
                status = request.GET.get('status1')

                return self.render_template(self.template_name,
                                               username=request.session['username'],
                                               messages=message,
                                               status=status,
                                               active=request.session['active_tab'],
                                               session_permission_list=request.session['session_permission_list'],
                                               google_analytics=request.session['google_analytics'])


            else:
                return self.redirect('/unauthorized/')
        else:
            return self.redirect('/unauthorized/')

class GetGridView(ViewBase):

    """
    Common Grid Rendering for dashboard and workload

    Attrubures:
        template_name: string
                       Holds 'work.mako' as string and used in get method for rendering
                       workload page
    """
    template_name = 'work.mako'

    def get(self, request):
        try:
            max = request.GET.get('max')
            offset = request.GET.get('offset')

            jobId = request.GET.get('jobId')
            userName = request.GET.get('userName')
            jobStatus = request.GET.get('status')
            jobState = request.GET.get('jobState')

            priorityFrom = request.GET.get('priorityFrom')
            priorityTo = request.GET.get('priorityTo')
            # Commenting code to remove rank columns --IRIS-309
            #rankFrom = request.GET.get('rankFrom')
            #rankTo = request.GET.get('rankTo')
            dateTimeRange = request.GET.get('dateTimeRange')
            startDate = request.GET.get('startDate')
            endDate = request.GET.get('endDate')
            wallclockStartDay = request.GET.get('wallclockStartDay')
            wallclockStartHr = request.GET.get('wallclockStartHr')
            wallclockStartMin = request.GET.get('wallclockStartMin')
            wallclockStartSec = request.GET.get('wallclockStartSec')
            wallclockEndDay = request.GET.get('wallclockEndDay')
            wallclockEndHr = request.GET.get('wallclockEndHr')
            wallclockEndMin = request.GET.get('wallclockEndMin')
            wallclockEndSec = request.GET.get('wallclockEndSec')

            if 'active_tab' in request.session:
                active_tab = request.session['active_tab']
            else:
                active_tab = "dashboard"

            query = []

            if userName is not None and userName != "null" and userName != '':
                query_userName = '{"user_name"' + ':{' + '"$like":"%25' + urllib.quote(userName.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_userName)

            if jobId is not None and jobId != '':
                query_jobId = '{"job_name":{"$like":"%25' + urllib.quote(jobId.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_jobId)

            if jobState is not None  and jobState != "null":
                query_jobState = '{"job_state"'+':'+'"'+str(jobState)+'"'+'},'
                query.append(query_jobState)

            # Commenting code to remove rank columns --IRIS-309
            """
            if rankTo and rankTo != u'0':
                if rankFrom and (int(rankTo) >= int(rankFrom)):
                    rank_string = '{"rank":{"$gte":'+str(rankFrom)+'}},{"rank":{"$lte":'+str(rankTo)+'}},'
                    query.append(rank_string)
            """

            # Commenting code to remove priority columns --IRIS-455
            """
            if priorityTo and priorityTo != u'0':
                if priorityFrom and (int(priorityTo) >= int(priorityFrom)):
                    priority_string = '{"priority":{"$gte":'+str(priorityFrom)+'}},{"priority":{"$lte":'+str(priorityTo)+'}},'
                    query.append(priority_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if priorityFrom != u'0' and priorityTo == u'0':
                priority_string = '{"priority":{"$gte":'+str(priorityFrom)+'}},'
                query.append(priority_string)
            """
            try:
                olddate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
                endDate = olddate + timedelta(seconds=1)
                endDate = unicode(endDate)
            except:
                pass

            if startDate and endDate != "null":
                if endDate >= startDate:
                    startTimeUTC = str(local_2_utc(startDate,request.session['timezone_offset']))
                    endTimeUTC = str(local_2_utc(endDate,request.session['timezone_offset']))
                    jobStartTimeQuery = '{"job_start_datetime":{"$gte":"' + startTimeUTC + ' UTC"}}'
                    jobEndTimeQuery = '{"job_start_datetime":{"$lt":"' + endTimeUTC + ' UTC"}},'
                    datetime_string = jobStartTimeQuery + ',' + jobEndTimeQuery
                    query.append(datetime_string)

            if startDate == ""  and endDate != "null" and endDate != "" :
                endTimeUTC = str(local_2_utc(endDate,request.session['timezone_offset']))
                datetime_string = '{"job_start_datetime":{"$lt":"'+ endTimeUTC +' UTC"}},'
                query.append(datetime_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if startDate != "null" and endDate == "" and startDate!= "":
                startTimeUTC = str(local_2_utc(startDate,request.session['timezone_offset']))
                datetime_string = '{"job_start_datetime":{"$gte":"'+ startTimeUTC +' UTC"}},'
                query.append(datetime_string)

            if wallclockStartDay and wallclockStartHr and wallclockStartMin and wallclockStartSec and wallclockEndDay and wallclockEndHr and wallclockEndMin and wallclockEndSec:
                totalstartseconds = int(wallclockStartDay) * 86400 + (int(wallclockStartHr)*3600) + (int(wallclockStartMin)*60) + (int(wallclockStartSec))
                totalendseconds = int(wallclockEndDay) * 86400 + (int(wallclockEndHr)*3600) + (int(wallclockEndMin)*60) + (int(wallclockEndSec))
                if totalendseconds >= totalstartseconds and totalendseconds != 0:
                    wallclockseconds_string = '{"wallclock_seconds":{"$gte":'+str(totalstartseconds)+'}},{"wallclock_seconds":{"$lte":'+str(totalendseconds)+'}},'
                    query.append(wallclockseconds_string)

                # Adding code Filters force user to enter max values --IRIS-333
                if totalstartseconds != 0 and totalendseconds == 0:
                    wallclockseconds_string = '{"wallclock_seconds":{"$gte":'+str(totalstartseconds)+'}},'
                    query.append(wallclockseconds_string)

            # This is to check redirection on job summary status state
            if jobStatus:
                if jobStatus == "notqueued":
                    jobStatus = "NotQueued"
                else:
                    jobStatus = str(jobStatus)

                jobStatus = '{"job_state"'+':'+'"'+ jobStatus +'"'+'},'

            # Setting offset value eg: if offset from the server is 1 then actual offset should be 0

            if offset and max:

                offset = int(offset) - 1

                # Getting Controls for pagination
                control = request.GET.get('control')
                if control == "goToFirst":
                    offset = 0
                elif control == "prev":
                    if int(offset) == 0:
                        offset = 0
                    else:
                        offset = int(offset) - 1
                elif control == "next":
                    lastOffset = request.GET.get('lastOffset')
                    if int(offset) == int(lastOffset)-1:
                        offset = int(lastOffset)-1
                    else:
                        offset = int(offset) + 1
                elif control == "goToLast":
                    lastOffset = request.GET.get('lastOffset')
                    offset = int(lastOffset) - 1
                offset_query = int(offset)*int(max)

            else:
                offset_query = ''



            # Sorting on different parameter according to state -1 descending a& +1 is ascending
            sort_parameter = request.GET.get('sort_parameter')
            sortState = request.GET.get('sortState')

            if sort_parameter:
                if sort_parameter == "job_name":
                    sort = {str("submit_datetime") :  int(sortState)}
                else:
                    sort = {str(sort_parameter) :  int(sortState)}
            else:
                sort = ''

            searchValue = request.GET.get('searchValue')
            searchCategory = request.GET.get('searchCategory')

            query_final = "".join(query)
            if searchValue:

                query_final = '{"' + str(searchCategory) + '":{"$like":"%25' + urllib.quote(searchValue.strip().encode('UTF-8')) + '%25"}}'

            query_set = {'sort' : sort, 'max' : max, 'offset' : offset_query, 'query' :query_final, 'jobStatus' : jobStatus}

            # Sending data ,count and status code
            workload_obj = WorkLoadDataView()
            workload_data, workload_data_count, status_code = workload_obj.get(request, query_set)


            for i in workload_data:
               if i['job_start_datetime']:
                    utcTime = i['job_start_datetime'].replace("UTC","").strip()
                    utcTime = datetime.strptime(utcTime, "%Y-%m-%d %H:%M:%S")
                    if 'timezone_offset' in request.session:
                        localTime = utc_2_local(utcTime,request.session['timezone_offset'])
                        i['job_start_datetime'] = localTime

            nums = ()
            if max:
                if workload_data_count > int(max):
                    range_para = int(math.ceil(float(workload_data_count)/float(max))) + 1
                    nums = range(1, range_para)
                else:
                    nums = range(1, 2)

            return self.render_template(self.template_name, status_code=status_code,
                                           total_count=workload_data_count,
                                           entries=workload_data,
                                           total_pages=len(nums),
                                           page_nums=nums,
                                           max=max,
                                           active=active_tab,
                                           offset=offset,
                                           session_permission_list=request.session['session_permission_list'],)
        except Exception as eX:
            APIError.debug_log(eX)
            return HttpResponse("Exception During data processing")

class GetWorkloadView(ViewBase):
    """
    Workload page rendering.

        Attrubures:
        template_name: string
                       Holds 'workload.mako' as string and used in get method
                       for rendering workload page
    """
    template_name = 'workload.mako'
    def get(self, request, *args, **kwargs):
        """
        Renders a workload page with username,password, session_permission_list etc.
        It sets request.session['path_previous'] as session variable using request.path

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse with workload related information like username,password,
            message,workload_filter etc and renders a workload page.Otherwise
            Redirect to unauthorized page.

        Raises:
            None
        """
        try:
            request.session['access_token']
            request.session['path_previous'] = request.path
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        status = request.GET.get('status1')
        if "session_permission_list" in request.session:
            if 'Workload' in request.session['session_permission_list']:
                message = ''
                storage = get_messages(request)
                for message in storage:
                    message = message
                request.session['active_tab'] = "workload"
                # This is to check redirection on job summary status state
                jobStatus = request.GET.get('status', "")
                return self.render_template(self.template_name, username=request.session['username'],
                                               statusCode=jobStatus,
                                               messages=message,
                                               status=status,
                                               active=request.session['active_tab'],
                                               session_permission_list=request.session['session_permission_list'],
                                               google_analytics=request.session['google_analytics'],
                                               workload_filter=WORKLOAD_FILTER_STATUS,)
            else:
                return self.redirect('/unauthorized/')
        else:
            return self.redirect('/unauthorized/')

class JobDetailsView(ViewBase):

    """
    Job Details Page rendering

    Attrubures:
            template_name_complete: string
                                                            Holds 'job_details.mako' as string and used in get and post
                                                            method for workload related functionality
            template_name_eligible: string
                                                            Holds 'job_details_pre.mako' as string and used in get
                                                            method for rendering workload page
    """
    template_name_complete = 'job_details.mako'
    template_name_eligible = 'job_details_pre.mako'
    @secured
    def get(self, request, *args, **kwargs):
        """
        Renders a job detail page with username,password and job detail related data.
        If any exception on getting  access token it sets request.session['path_previous']
        as session varible and redirect to login page.

        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse with job detail related information like username,password,
                message etc and renders a job detail page.Otherwise any exception getting
                access token redirect to login page.
                Redirect to workload page if job_name,job_status,job_id not found

        Raises:
                None
        """

        job_name = request.GET.get('job_name')
        job_status = request.GET.get('job_status')
        job_id = request.GET.get('job_id')
        status = request.GET.get('status1')
        storage_messages = request.GET.get('storage_messages')
        if not job_name or not job_status or not job_id:
            request.session['path_previous'] = request.path
            # Job id not specified so redirect to workload page with error
            messages.add_message(request, messages.ERROR, ugettext("Job id must be specified to view details"))
            return self.redirect_to_name("workload")

        message = ''

        # This view gets the complete job details data for particular job_name
        jobviewGet_obj = JobDetailsGetDataView()
        job_data, success_status = jobviewGet_obj.get(request, job_name)

        nodelist_required = []
        requiredfeatures_data = []
        requirements = []
        data_resourcelist = []
        features = ""
        nodelist_allocated = ""
        generic_resourceslist = ""
        duration_format = '00:00:00:00'
        actualduration_format = '00:00:00:00'
        FMT = '%Y-%m-%d %H:%M:%S'
        # checking success status
        if success_status == 2000 and job_data:
            storage = get_messages(request)
            for message in storage:
                message = message

            if job_data[0]['requested_features'] is not None:
                features = job_data[0]['requested_features'].split(',')
                features = [i.strip() for i in features]

            if job_data[0]['generic_resource_name']:
                generic_resourceslist = job_data[0]['generic_resource_name'].split(',')

            if job_data[0]['wallclock_seconds']:
                wallclock_sec = job_data[0]['wallclock_seconds']
                sec = timedelta(seconds=int(wallclock_sec))
                d = datetime(1, 1, 1) + sec
                days = int(wallclock_sec)/86400
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


                duration_format = str(days) +":" +str(hours) +":"+ str(minutes)+":"+ str(seconds)

            #converting the starttime to local time for display
            if job_data[0]['start_datetime']:
                if 'timezone_offset' in request.session:
                    utcTime = job_data[0]['start_datetime'].replace("UTC","").strip()
                    job_data[0]['start_datetime'] = utc_2_local(utcTime, request.session['timezone_offset'])

             #converting the completion time to local time for display
            if job_data[0]['completion_datetime']:
                if 'timezone_offset' in request.session:
                    utcTime = job_data[0]['completion_datetime'].replace("UTC","").strip()
                    job_data[0]['completion_datetime'] = utc_2_local(utcTime, request.session['timezone_offset'])



            #Actual Duration  Time calculated depending on the states of jobs.If state is completed , elapsed time is the difference between the current time and the job start time.
            if job_data[0]['state'] in ("RUNNING", "STAGING", "STARTING"):
                if job_data[0]['start_datetime']:
                    tdelta = datetime.strptime(re.sub("\.\d*.*$", "", str(timezone.now())), FMT) - datetime.strptime(re.sub("\ \w*$", "", str(job_data[0]['start_datetime'])), FMT)
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
                    actualduration_format = str(days) +":" +str(hours) +":"+ str(minutes)+":"+ str(seconds)

                else:
                    actualduration_format = '-'


            elif job_data[0]['state'] in ("COMPLETED", "FAILED", "REMOVED", "VACATED"):
                if job_data[0]['start_datetime'] and job_data[0]['completion_datetime']:
                    tdelta = datetime.strptime(re.sub("\ \w*$", "", str(job_data[0]['completion_datetime'])), FMT) - datetime.strptime(re.sub("\ \w*$", "", str(job_data[0]['start_datetime'])), FMT)
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
                    actualduration_format = str(days) +":" +str(hours) +":"+ str(minutes)+":"+ str(seconds)

                else:
                    actualduration_format = '-'

            else:
                actualduration_format = '-'

            '''
            if job_data[0]['start_datetime']:
                start_datetime = re.sub(" \w{3}", "", job_data[0]['start_datetime'])
                current_time = re.sub("\.\d{3,}.*$", "", str(timezone.now()))
                tdelta = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
                e = datetime(1, 1, 1) + timedelta(seconds=int(tdelta.seconds))
                if int(tdelta.days) < 10:
                    days = "0" + str(tdelta.days)
                hours = e.hour
                if int(hours) < 10:
                    hours = "0" + str(hours)
                minutes = e.minute
                if int(minutes) < 10:
                    minutes = "0" + str(minutes)

                seconds = e.second
                if int(seconds) < 10:
                    seconds = "0" + str(seconds)

                actualduration_format = str(days) +":" +str(hours) +":"+ str(minutes)+":"+ str(seconds)

            if job_data[0]['start_datetime'] is None:
                actualduration_format = "00:00:00:00"
            '''

            if job_data[0]['allocated_node_list']:
                nodelist_allocated = job_data[0]['allocated_node_list'].split(',')

            if job_data[0]['required_node_list']:
                nodelist_required = job_data[0]['required_node_list'].split(',')
                nodelist_required = [i.strip() for i in nodelist_required]

            #get job multi requirements
            requirements_data = JobDetailsMultiReqDataView()
            requirements, statusCode = requirements_data.get(request, job_name)

            if statusCode != 200:
                requirements = []

             #Storing the editable fields value in session variable
            request.session['duration_format_'+str(job_data[0]['name'])] = duration_format
            request.session['qos_'+str(job_data[0]['name'])] = job_data[0]['qos_name']
            request.session['job_priority_'+str(job_data[0]['name'])] = job_data[0]['run_priority']
            request.session['system_priority_'+str(job_data[0]['name'])] = job_data[0]['system_priority']
            request.session['custom_name_'+str(job_data[0]['name'])] = job_data[0]['custom_name']
            request.session['required_nodelist_'+str(job_data[0]['name'])] = nodelist_required
            request.session['required_fetaures_'+str(job_data[0]['name'])] = features

            resourcelist_obj = ResourceListDataView()
            resourcelist_data  ,resourcelist_data_count, status_code = resourcelist_obj.get(request)

            # Adding code for -IRIS-451
            if status_code > -1:
                for i in resourcelist_data:
                    data_resourcelist.append(i["name"])

        else:
            # Job doesn't exist so redirect to workload page with error
            messages.add_message(request, messages.ERROR, ugettext("Job '{0}' does not exist").format(job_name))
            return self.redirect_to_name("workload")


        # Move to utils
        if job_status in ("COMPLETED", "RUNNING", "FAILED", "REMOVED", "STARTING", "STAGING", "VACATED"):
            tpl = self.template_name_complete

            #elif job_status in  "BatchHold" or job_status == "Blocked" or job_status == "Deferred" or job_status == "Hold" or job_status == "Idle" or job_status == "NotQueued" or job_status == "Suspended" or job_status == "SystemHold" or job_status == "Unknown" or job_status == "UserHold":
        else:
            # This view gets the all Required Features Data
            requiredfeatures_obj = RequiredFeaturesDataView()
            requiredfeatures_data = requiredfeatures_obj.get(request)

            # Adding code for -IRIS-451
            if not isinstance(requiredfeatures_data, str):
                for i in requiredfeatures_data:
                    i['feature'] = i['feature'].strip()


            # This view gets the all Generic Resource Data .Currently commenting out this as MOAB does not allow generic resources modification
            #genericresoucres_obj = GenericResourceDataView()
            #genericresoucres_data = genericresoucres_obj.get(request)

            tpl = self.template_name_eligible
        return self.render_template(tpl,username=request.session['username'],
                                       entries=job_data,
                                       nodelist_allocated=nodelist_allocated,
                                       duration_format=duration_format,
                                       actualduration_format=actualduration_format,
                                       status_code=success_status,
                                       featurelist=features,
                                       generic_resourceslist=generic_resourceslist,
                                       job_id=job_id,
                                       job_status=job_status,
                                       required_nodelist=nodelist_required,
                                       requiredfeatures=requiredfeatures_data,
                                       node_list = data_resourcelist,
                                       job_requirements = requirements,
                                       hasMultiReqs = (len(requirements) > 1),
                                       #genericresoucres = genericresoucres_data,
                                       status = status,
                                       messages=message,
                                       storage_messages=storage_messages,
                                       session_permission_list=request.session['session_permission_list'],
                                       google_analytics=request.session['google_analytics'])
    @secured
    def post(self, request, *args, **kwargs):
        """
        Renders a job detail page with username,password and job detail related data.
        If any exception on getting  access token it sets request.session['path_previous']
        as session varible and redirect to login page.

        Args:
                        request: represents a single HTTP request. Request objects also have
                                                         a few useful methods like GET,POST,DELETE etc.

                        *args: Variable length argument list.

                        **kwargs: Arbitrary keyword arguments.

        Returns:
                        HttpResponse with job detail related information like username,password,
                        message etc and renders a job detail page.
                        Redirect to login page if any eception getting access token.
                        Redirect to workload page if job_name,job_status,job_id not found

        Raises:
                        None
        """

        # This fields are required for redirection logic for jobdetails apply form post to jobdetails get view
        job_name = request.POST.get('job_name').strip()
        custom_name = ""


        job_status = request.POST.get('job_status')
        job_id = request.POST.get('job_id')

        # This field is required for redirection for done and apply
        action = request.POST.get('action')
        qos_name = str(request.POST.get('qos'))
        duration = request.POST.get('duration')
        nodeList = request.POST.get('nodeList')
        run_priority = request.POST.get('job_priority')
        system_priority = request.POST.get('sys_priority')
        requested_features = request.POST.get('featureList')
        addResource = request.POST.get('resourceList')
        prvpath = request.POST.get('prvpath')
        isMultiReqJob = request.POST.get('isMultiReqJob')

        priority_dict = {}
        priorities_dict = {}
        requested_features_list = []


        #Dictionary created for nodes that has to be sent in the json format push
        resourcesPerTask = {}
        dedicated_dict = {"dedicated":""}

        #List for nodes
        nodelist_array = []
        node_features_list = []
        # Defined keys to avoid key errors
        format_raw_json = {}


        if qos_name is not None and qos_name != "None":
            if qos_name != request.session['qos_'+str(job_name)]:
                qos_dict = {"credentials": {"qosRequested": qos_name}}
                format_raw_json.update(qos_dict)

        if custom_name:
            if custom_name != request.session['custom_name_'+str(job_name)]:
                custom_dict = {"customName": "Sample"}
                format_raw_json.update(custom_dict)

        if duration:
            if duration != request.session['duration_format_'+str(job_name)]:
                duration_cal = duration.split(":")
                wallclock_seconds = int(duration_cal[0]) * 86400 + (int(duration_cal[1])*3600) + (int(duration_cal[2])*60) + (int(duration_cal[3]))
                duration_dict = {"duration": wallclock_seconds}
                format_raw_json.update(duration_dict)

        if nodeList:
            nodelist_array = nodeList.split(",")
        else:
            nodelist_array = []

        if sorted(nodelist_array) != sorted(request.session['required_nodelist_'+str(job_name)]):
            if nodelist_array:
                for i in nodelist_array:
                    nodes_dict = {}
                    nodes_dict["name"] = i.encode("utf-8")
                    node_features_list.append(nodes_dict)
            else:
                nodes_dict = {}
                node_features_list.append(nodes_dict)
            nodesrequested_dict = {"nodesRequested": node_features_list}
            format_raw_json.update(nodesrequested_dict)

        if run_priority:
            if int(run_priority) != request.session['job_priority_'+str(job_name)]:
                priority_dict['user'] = str(run_priority)

        if system_priority:
            if int(system_priority) != request.session['system_priority_'+str(job_name)]:
                priority_dict['system'] = str(system_priority)


        if priority_dict:
            priorities_dict = {"priorities" : priority_dict}
            format_raw_json.update(priorities_dict)




        if not job_status in ("COMPLETED", "RUNNING", "FAILED", "REMOVED", "STARTING", "STAGING", "VACATED"):
            if requested_features:
                req_features_list = requested_features.split(",")
                req_features_list = [i.strip() for i in req_features_list]
            else:
                req_features_list = []

            if isMultiReqJob != "True" and (sorted(req_features_list) != sorted(request.session['required_fetaures_'+str(job_name)])) :
                for i in req_features_list:
                    requested_features_list.append(str(i))
                requiredfeatures_list = []
                features_main_dict = {}
                features_dict = {"features": requested_features_list}
                requiredfeatures_list.append(dict(features_dict))
                features_main_dict = {"requirements" : requiredfeatures_list}
                format_raw_json.update(features_main_dict)

        #Commenting out these Generic Resources code for the time being as the option of editing these are removed from UI
        '''
        if addResource:
            addResource_list = addResource.split(",")
            for i in addResource_list:
                resourcesPerTask[i.encode("utf-8")] = dedicated_dict
        '''

        # This view post the details for job details to modify particular job_name
        jobviewPost_obj = JobDetailsPostDataView()

        response_message, status = jobviewPost_obj.get(request, job_name, format_raw_json)
        messages.success(request, response_message)
        if action == "Apply":
            if request.session.has_key('active_tab'):
                return self.redirect(reverse("jobdetails") + "?job_name="+str(job_name)+"&job_status="+str(job_status)+"&job_id="+str(job_id)+"&prvpath="+str(prvpath)+"&tab="+str(request.session['active_tab']+"&status1="+str(status)))
            else:
                return self.redirect_to_name('login')

        else:
            # IF action id Done redirect to workload without display of a message
            if request.session.has_key('path_previous'):
                return self.redirect(request.session['path_previous']+"?status1="+str(status))
            else:
                return self.redirect(reverse("workload")+"?status1="+str(status))

class GenerateReportsView(ViewBase):
    """
    Reports Generation csv & xml

    Attrubures:
        None
    """
    def get(self, request, *args, **kwargs):
        """
        Report generation related funationality.
        This funtion includes  csv and xml file creation funationality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            For csv format it sets all header labels with job detail related data
            and returns in HttpResponse.
            For xml format it collect all data related to job detail and redirect to
            download path to open newly  created xml page.

        Raises:
            Appropriate exception during file writing opreation.

        """
        format = request.GET.get('format')

        reports_obj = GenerateReportsDataView()
        reports_data = reports_obj.get(request)
        import datetime
        current_date = datetime.date.today()
        filename = "JobRecordsFor-" + str((current_date).strftime("%d-%m-%Y"))
        if not isinstance(reports_data, str):
            if format == 'csv':
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
                writer = csv.writer(response, csv.excel)
                headers = [ugettext('Job_ID'), ugettext('Job_Name'), ugettext('Submitter_ID'), ugettext('Job_Custom_Name'), ugettext('Job_State'),
                           ugettext('Priority'), ugettext('Rank'), ugettext('Resources'), ugettext('Resource_States'),
                           ugettext('Utilized_Processor_Seconds'), ugettext('Utilized_Memory_Seconds'),
                           ugettext('Wallclock_Seconds'), ugettext('Job_Sort'), ugettext('Job_Start_Datetime')
                          ]

                writer.writerow(headers)
                for records in reports_data.data:
                    writer.writerow([str(records['job_id']),
                                     str(records['job_name']),
                                     str(records['user_name']),
                                     str(records['job_custom_name']),
                                     str(records['job_state']),
                                     str(records['priority']),
                                     str(records['rank']),
                                     str(records['resources']),
                                     str(records['resource_states']),
                                     str(records['utilized_processor_seconds']),
                                     str(records['utilized_memory_seconds']),
                                     str(records['wallclock_seconds']),
                                     str(records['job_sort']),
                                     str(records['job_start_datetime']),])
                return response
            elif format == 'xml':
                result = []
                response = HttpResponse(mimetype='text/xml')
                response['Content-Disposition'] = 'attachment; filename=' + filename + '.xml'
                root = ET.Element(ugettext('root'))
                for records in reports_data.data:
                    job = ET.SubElement(root, ugettext('Job'))
                    jobid = ET.SubElement(job, ugettext('Job_ID'))
                    jobid.text = str(records['job_id'])
                    job_name = ET.SubElement(job, ugettext('Job_Name'))
                    job_name.text = str(records['job_name'])
                    jobid = ET.SubElement(job, ugettext('Submitter_ID'))
                    jobid.text = str(records['user_name'])
                    job_custom_name = ET.SubElement(job, ugettext('Job_Custom_Name'))
                    job_custom_name.text = str(records['job_custom_name'])
                    job_state = ET.SubElement(job, ugettext('Job_State'))
                    job_state.text = str(records['job_state'])
                    priority = ET.SubElement(job, ugettext('Priority'))
                    priority.text = str(records['priority'])
                    rank = ET.SubElement(job, ugettext('Rank'))
                    rank.text = str(records['rank'])
                    resources = ET.SubElement(job, ugettext('Resources'))
                    resources.text = str(records['resources'])
                    resource_states = ET.SubElement(job, ugettext('Resource_States'))
                    resource_states.text = str(records['resource_states'])
                    utilized_processor_seconds = ET.SubElement(job, ugettext('Utilized_Processor_Seconds'))
                    utilized_processor_seconds.text = str(records['utilized_processor_seconds'])
                    utilized_memory_seconds = ET.SubElement(job, ugettext('Utilized_Memory_Seconds'))
                    utilized_memory_seconds.text = str(records['utilized_memory_seconds'])
                    wallclock_seconds = ET.SubElement(job, ugettext('Wallclock_Seconds'))
                    wallclock_seconds.text = str(records['wallclock_seconds'])
                    user_name = ET.SubElement(job, ugettext('User_Name'))
                    user_name.text = str(records['user_name'])
                    job_sort = ET.SubElement(job, ugettext('Job_Sort'))
                    job_sort.text = str(records['job_sort'])
                    job_start_datetime = ET.SubElement(job, ugettext('Job_Start_Datetime'))
                    job_start_datetime.text = str(records['job_start_datetime'])
                tree = ET.ElementTree(root)
                tree.write(response)
                return response
        else:
            return HttpResponse(reports_data)

class ModifyJobsView(ViewBase):
    """
    This class handles the request for change on job status
    """
    def get(self, request, *args, **kwargs):
        """
        Modify job status of perticular job by using job id

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse response_message when job modify.
            Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        jobId = request.GET.get('jobId')
        changeStatus = request.GET.get('changeStatus')
        status_obj = ModifyJobsStatusView()
        response_message, status = status_obj.get(request, jobId, changeStatus)

        return HttpResponse(response_message+","+str(status))
