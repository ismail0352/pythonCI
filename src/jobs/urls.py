# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.conf.urls import patterns, url

from jobs.views import GetWorkloadView, GetGridView, GetDashboardView, \
    JobDetailsView, GenerateReportsView, ModifyJobsView


urlpatterns = patterns('',
                       url(r'^workload/$', GetWorkloadView.as_view(), name='workload'),
                       url(r'^workload_table/$', GetGridView.as_view(), name='workload_table'),
                       url(r'^dashboard/$', GetDashboardView.as_view(), name='dashboard'),
                       url(r'^jobdetails/$', JobDetailsView.as_view(), name='jobdetails'),
                       url(r'^generateReports/$', GenerateReportsView.as_view(), name='generatereports'),
                       url(r'^modifyjob/$', ModifyJobsView.as_view(), name='modifyjob'),
)
