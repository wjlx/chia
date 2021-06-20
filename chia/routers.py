#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

# from rest_framework_swagger.views import get_swagger_view


router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    url('plots/', include('apps.plots.urls')),
]

# if settings.SHOW_DOC:
#     schema_view = get_swagger_view(title='爱点读API')
#     urlpatterns += [url('^docs/$', schema_view)]
