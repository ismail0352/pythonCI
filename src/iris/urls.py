# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""

from django.conf.urls import patterns, include, url

from django.conf import settings

handler404 = 'login.utils.Error404'
handler500 = 'login.utils.Error500'
handler403 = 'login.utils.Error403'
handler400 = 'login.utils.Error400'
handler401 = 'login.utils.Error401'

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)), 
                       url(r'^', include('login.urls')),                      
                       url(r'^api/', include('api.urls')),
                       url(r'^', include('configuration.urls')),
                       url(r'^', include('nodes.urls')),
                       url(r'^', include('jobs.urls')),                                            
)

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)

