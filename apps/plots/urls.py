# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

# from rest_framework import routers
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

# router = routers.DefaultRouter()
# router.register(r'user_key', UserKeyViewSet)
# router.register(r'plots_task', PlotsTaskViewSet)
# router.register(r'plots_task_control', PlotsTaskControlViewSet)
# router.register(r'plots_task_result', PlotsTaskResultViewSet)
#
# urlpatterns = router.urls

methods = {
    'get': 'list',
    'post': 'create',
    'put': 'update'
}


def _(*args):
    return dict([(i, methods[i]) for i in args])


urlpatterns = [
    # 用户
    url(r'^user/$', UserView.as_view(_('get', 'post'))),
    url(r'^user/(?P<pk>[0-9]+)$', UserView.as_view(_('put'))),

    url(r'^user_key/$', UserKeyViewSet.as_view(_('get', 'post'))),
    url(r'^user_key/(?P<pk>[0-9]+)$', UserKeyViewSet.as_view(_('put'))),

    url(r'^plots_task/$', PlotsTaskViewSet.as_view(_('get', 'post'))),
    url(r'^plots_task/(?P<pk>[0-9]+)$', PlotsTaskViewSet.as_view(_('put'))),

    url(r'^plots_task_control/$', PlotsTaskControlViewSet.as_view(_('get', 'post'))),
    url(r'^plots_task_control/(?P<pk>[0-9]+)$', PlotsTaskControlViewSet.as_view(_('put'))),

    url(r'^plots_task_result/$', PlotsTaskResultViewSet.as_view(_('get', 'post'))),
    url(r'^plots_task_result/(?P<pk>[0-9]+)$', PlotsTaskResultViewSet.as_view(_('put'))),
]

urlpatterns = format_suffix_patterns(urlpatterns)
