# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'user_key', UserKeyViewSet)
router.register(r'plots_task', PlotsTaskViewSet)
router.register(r'plots_task_control', PlotsTaskControlViewSet)
router.register(r'plots_task_result', PlotsTaskResultViewSet)

urlpatterns = router.urls
