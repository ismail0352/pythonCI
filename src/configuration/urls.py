# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.conf.urls import patterns, url

from configuration.views import GetConfigurationView, RoleManagementCreate, \
    RoleManagementDelete, RoleListView, RoleListGridView, PrincipalListView, \
    PrincipalGridView, GetPrincipalCreateEditView, GetPrincipalDeleteView


urlpatterns = patterns('',
                       url(r'^configuration/$', GetConfigurationView.as_view(), name='configuration'),
                       url(r'^createrole/$', RoleManagementCreate.as_view(), name="createrole"),
                       url(r'^deleterole/$', RoleManagementDelete.as_view(), name="deleterole"),
                       url(r'^rolelist/$', RoleListView.as_view(), name="rolelist"),
                       url(r'^rolelist_grid/$', RoleListGridView.as_view(), name="rolelistgrid"),
                       url(r'^principallist/$', PrincipalListView.as_view(), name="principallist"),
                       url(r'^principallist_grid/$', PrincipalGridView.as_view(), name="principallistgrid"),
                       url(r'^principal/$', GetPrincipalCreateEditView.as_view(), name="principal"),
                       url(r'^deleteprincipal/$', GetPrincipalDeleteView.as_view(), name="principaldelete"),

)
