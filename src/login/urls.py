# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.conf.urls import patterns, url

from login.utils import Error401
from login.views import Login, Logout


urlpatterns = patterns('',
                       url(r'^$', Login.as_view(), name='login_root'),
                       url(r'^logout/$', Logout.as_view(), name='logout'),
                       url(r'^login/$', Login.as_view(), name='login'),
                       url(r'^unauthorized/$', Error401, name="unauthorized"),
)
