# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.conf.urls import patterns, url
from nodes.views import GetResourceListView, GetResouceGridView, NodeDetailsView


urlpatterns = patterns('',
                       url(r'^nodelist/$', GetResourceListView.as_view(), name='nodelist'),
                       url(r'^node_table/$', GetResouceGridView.as_view(), name='node_table'),
                       url(r'^nodedetails/$', NodeDetailsView.as_view(), name='nodedetails'),
)
