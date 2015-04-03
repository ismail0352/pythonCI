# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import math
import urllib

from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.utils.translation import ugettext

from api.nodes.views import ResourceListDataView, NodeDetailsDataView, \
    ConfigurableFeaturesDataView, GenericResourcePerNodeDataView
from frontend_utils.view_base import ViewBase
from login.utils import RESOURCE_FILTER_STATUS, APIError


class GetResourceListView(ViewBase):
    """
    This class handles the request for change on Node Listing

    Attrubutes:
        template_name = string
                        Holds 'nodelist.mako' and used in get method for
                        rendering nodelist page
    """
    template_name = 'nodelist.mako'
    def get(self, request, *args, **kwargs):
        """
        Shows resource list

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse and render nodelist.mako page
            Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        status = request.GET.get("status1")
        if "session_permission_list" in request.session:
            if 'Resources' in request.session['session_permission_list']:
                message = ''
                storage = get_messages(request)
                for message in storage:
                    message = message

                request.session['active_tab'] = "resources"

                jobStatus = request.GET.get('status', '')
                status_code = request.GET.get('status_code','')
                return self.render_template(self.template_name, username=request.session['username'],
                                               jobStatus=jobStatus,
                                               status_code = status_code,
                                               session_permission_list=request.session['session_permission_list'],
                                               messages=message,
                                               status=status,
                                               google_analytics=request.session['google_analytics'],
                                               resource_filter=RESOURCE_FILTER_STATUS,)
            else:
                return self.redirect('/unauthorized/')
        else:
            return self.redirect('/unauthorized/')

class GetResouceGridView(ViewBase):
    """
    Grid Rendering for Node List Page

    Attrubutes:
        template_name_resourcelistgrid = string
                                          Holds 'node_grid.html' and used in get method for
                                          rendering resource grid in nodelist page
    """
    template_name_resourcelistgrid = 'node_grid.html'
    def get(self, request):
        """
        Shows resource list
        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse and render node_grid page.
                HttpResponse if any exception in ResourceListDataView

        Raises:
                None

        """
        try:
            max = request.GET.get('max')
            offset = request.GET.get('offset')
            jobStatus = request.GET.get('status')
            name = request.GET.get('name')
            state = request.GET.get('state')
            classes = request.GET.get('classes')
            features = request.GET.get('features')
            procsFrom = request.GET.get('procsFrom')
            procsTo = request.GET.get('procsTo')
            jobsFrom = request.GET.get('jobsFrom')
            jobsTo = request.GET.get('jobsTo')
            proc_utilFrom = request.GET.get('proc_utilFrom')
            proc_utilTo = request.GET.get('proc_utilTo')
            memory_utilFrom = request.GET.get('memory_utilFrom')
            memory_utilTo = request.GET.get('memory_utilTo')
            if 'active_tab' in request.session:
                active_tab = request.session['active_tab']
            else:
                active_tab = "resources"
            query = []
            if name is not None and name != "null" and name != '':
                query_ResourceId = '{"name":{"$like":"%25' + urllib.quote(name.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_ResourceId)
            if state is not None and state is not u'' and state != "null":
                query_state = '{"state":{"$like":"%25' + urllib.quote(state.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_state)
            if classes is not None and classes != "null" and classes != '':
                query_classes = '{"classes":{"$like":"%25' + urllib.quote(classes.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_classes)
            if features is not None and features != "null" and features != '':
                query_features = '{"features":{"$like":"%25' + urllib.quote(features.strip().encode('UTF-8')) + '%25"}},'
                query.append(query_features)
            if procsTo and procsTo != u'0':
                if procsFrom and (int(procsTo) >= int(procsFrom)):
                    procs_string = '{"processors":{"$gte":'+str(procsFrom)+'}},{"processors":{"$lte":'+str(procsTo)+'}},'
                    query.append(procs_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if procsFrom != u'0' and procsTo == u'0':
                procs_string = '{"processors":{"$gte":'+str(procsFrom)+'}},'
                query.append(procs_string)

            if jobsTo and jobsTo != u'0':
                if jobsFrom and (int(jobsTo) >= int(jobsFrom)) and jobsTo is not None:
                    jobs_string = '{"jobs":{"$gte":'+str(jobsFrom)+'}},{"jobs":{"$lte":'+str(jobsTo)+'}},'
                    query.append(jobs_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if jobsFrom != u'0' and jobsTo == u'0':
                jobs_string = '{"jobs":{"$gte":'+str(jobsFrom)+'}},'
                query.append(jobs_string)

            if proc_utilTo and proc_utilTo != u'0':
                if proc_utilFrom and (int(proc_utilTo) >= int(proc_utilFrom)):
                    proc_util_string = '{"processor_utilization_percentage":{"$gte":'+str(proc_utilFrom)+'}},{"processor_utilization_percentage":{"$lte":'+str(proc_utilTo)+'}},'
                    query.append(proc_util_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if proc_utilFrom != u'0' and proc_utilTo == u'0':
                proc_util_string = '{"processor_utilization_percentage":{"$gte":'+str(proc_utilFrom)+'}},'
                query.append(proc_util_string)

            if memory_utilTo and memory_utilTo != u'0':
                if memory_utilFrom and (int(memory_utilTo) >= int(memory_utilFrom)):
                    memory_util_string = '{"memory_utilization_percentage":{"$gte":'+str(memory_utilFrom)+'}},{"memory_utilization_percentage":{"$lte":'+str(memory_utilTo)+'}},'
                    query.append(memory_util_string)

            # Adding code Filters force user to enter max values --IRIS-333
            if memory_utilFrom != u'0' and memory_utilTo == u'0':
                memory_util_string = '{"memory_utilization_percentage":{"$gte":'+str(memory_utilFrom)+'}},'
                query.append(memory_util_string)

            # This is to check redirection on job summary status state
            if jobStatus:
                jobStatus = '{"state"'+':'+'"'+str(jobStatus)+'"'+'},'
            if offset and max:
                # Setting offset value eg: if offset from the server is 1 then actual offset should be 0
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
                        offset = (int(lastOffset)-1)
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
                sort = {str(sort_parameter) :  int(sortState)}
            else:
                sort = ''
            query_final = "".join(query)
            query_set = {'sort' : sort, 'max' : max, 'offset' : offset_query, 'query' :query_final, 'jobStatus' : jobStatus}
            resourcelist_obj = ResourceListDataView()
            # Sending data , count and status code
            resourcelist_data, resourcelist_data_count, status_code = resourcelist_obj.get(request, query_set)
            nums = ()
            if max:
                if resourcelist_data_count > int(max):
                    range_para = int(math.ceil(float(resourcelist_data_count)/float(max))) + 1
                    nums = range(1, range_para)
                else:
                    nums = range(1, 2)
            return self.render_template(self.template_name_resourcelistgrid, status_code=status_code,
                                           total_count=resourcelist_data_count,
                                           entries=resourcelist_data,
                                           total_pages=len(nums),
                                           page_nums=nums,
                                           max=max,
                                           offset=offset,
                                           active=active_tab,
                                           session_permission_list=request.session['session_permission_list'],)
        except Exception as eX:
            APIError.debug_log(eX)
            return HttpResponse("Exception During data processing")

class NodeDetailsView(ViewBase):
    """
    Node Details Page rendering

    Attrubutes:
    template_name = string
                                    Holds 'nodedetails.mako' and used in get and post method for
                                    rendering node detail view in nodedetails page

    """
    template_name = 'nodedetails.mako'
    def get(self, request, *args, **kwargs):
        """
        Shows node detail in nodes page
        It loads node data from NodeDetailsDataView with success_code.

        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse and render node detail page by using node name.
                Redirect to login page if access token not found.

        Raises:
                None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        node_name = request.GET.get('node_name')
        if node_name:
            node_name = node_name.strip()

        message = ''
        storage = get_messages(request)
        for message in storage:
            message = message

        status = request.GET.get("status1")
        nodeview_obj = NodeDetailsDataView()
        node_data, success_status = nodeview_obj.get(request, node_name)
        configurablefeatures = []
        featurelist = ""
        torquelist = ""
        configurablefeatures_data = []
        genericresourcespernode_data = []
        # checking success status
        if success_status == 2000 and node_data:
            storage = get_messages(request)
            for message in storage:
                message = message

            if node_data[0]['configurable_features']:
                configurablefeatures = node_data[0]['configurable_features'].split(",")
                configurablefeatures = [i.strip() for i in configurablefeatures]

            # Calling configurable Features api
            configurablefeatures_obj = ConfigurableFeaturesDataView()
            configurablefeatures_data = configurablefeatures_obj.get(request)

            if configurablefeatures_data:
                for i in configurablefeatures_data:
                    i['feature'] = i['feature'].strip()

            if node_data[0]['features_reported']:
                featurelist = node_data[0]['features_reported'].split(',')
            else:
                featurelist = node_data[0]['features_reported']

            if node_data[0]['resource_managers']:
                torquelist = node_data[0]['resource_managers'].split(',')

            request.session['config_list'+str(node_data[0]['name'])] = configurablefeatures


            #Calling the Generic Resourcs Per Node api
            genericresourcespernode_obj = GenericResourcePerNodeDataView()
            genericresourcespernode_data = genericresourcespernode_obj.get(request, node_name)

        else:
            # Node doesn't exist so redirect to  resource page with error
            messages.add_message(request, messages.ERROR, ugettext("Node '{0}' does not exist").format(node_name))
            return self.redirect("/nodelist/")

        return self.render_template(self.template_name, success_status=success_status,
                                       username=request.session['username'],
                                       entries=node_data,
                                       status_code=success_status,
                                       torquelist=torquelist,
                                       featurelist=featurelist,
                                       session_permission_list=request.session['session_permission_list'],
                                       config_features_list=configurablefeatures_data,
                                       config_features=configurablefeatures,
                                       generic_resources=genericresourcespernode_data,
                                       messages=message,
                                       status=status,
                                       google_analytics=request.session['google_analytics'],)

    def post(self, request, *args, **kwargs):
        """
        Modify job name

        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                If action is 'Apply' it redirect node detail page otherwise
                it renders a resource list page

        Raises:
                None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        # This fields are required for redirection logic for node details apply form post to nodedetails get view
        node_name = request.POST.get('node_name')
        action = request.POST.get('action')
        # This field is required for redirection for done and apply
        requested_features = request.POST.get('cfList')

        if requested_features:
            req_features_list = requested_features.split(",")
        else:
            req_features_list = []

        node_features_json = {}
        if req_features_list != request.session['config_list'+str(node_name)]:
            node_features_json = {"featuresCustom": req_features_list}

        # This view post the details for job details to modify particular job_name
        nodeviewPost_obj = NodeDetailsDataView()

        response_message, status = nodeviewPost_obj.post(request, node_name, node_features_json)
        messages.success(request, response_message)
        if action == "Apply":
            return self.redirect("/nodedetails/?node_name="+str(node_name)+"&tab=resources&status1="+str(status))
        else:
            return self.redirect("/nodelist/?status1="+str(status))
