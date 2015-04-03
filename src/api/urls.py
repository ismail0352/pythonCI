# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.conf.urls import patterns, url

from api.jobs.views import WorkLoadDataView, JobSummaryDataView, \
    SystemUtilizationDataView, JobDetailsGetDataView
from api.nodes.views import ResourceSummaryDataView, NodeDetailsDataView, \
    ResourceListDataView


urlpatterns = patterns('',
                       url(r'^getworkload/$', WorkLoadDataView.as_view(), name="WorkLoadDataView"),
                       url(r'^getjobsummary/$', JobSummaryDataView.as_view(), name="JobSummaryDataView"),
                       url(r'^getresourcesummary/$', ResourceSummaryDataView.as_view(), name="ResourceSummaryDataView"),
                       url(r'^getsystemutilization/$', SystemUtilizationDataView.as_view(), name="SystemUtilizationDataView"),
                       url(r'^getnodedetails/$', NodeDetailsDataView.as_view(), name="NodeDetailsDataView"),
                       url(r'^getjobdetails/$', JobDetailsGetDataView.as_view(), name="JobeDetailsGetDataView"),
                       url(r'^getnodelist/$', ResourceListDataView.as_view(), name="ResourceListDataView"),

)
