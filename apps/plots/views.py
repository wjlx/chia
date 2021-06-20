# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from apps.base.views import BaseModelViewSet
from .filters import *
from .serializers import *


class UserKeyViewSet(BaseModelViewSet):
    """
    用户秘钥
    """
    queryset = UserKey.objects.all().order_by('-update_at')
    serializer_class = UserKeySerializer
    # filter_backends = [UserKeyFilter]
    filter_class = UserKeyFilter


class PlotsTaskViewSet(BaseModelViewSet):
    """
    用户秘钥
    """
    queryset = PlotsTask.objects.all().order_by('-update_at')
    serializer_class = PlotsTaskSerializer
    # filter_backends = [PlotsTaskFilter, ]
    filter_class = PlotsTaskFilter


class PlotsTaskControlViewSet(BaseModelViewSet):
    """
    用户秘钥
    """
    queryset = PlotsTaskControl.objects.all().order_by('-update_at')
    serializer_class = PlotsTaskControlSerializer
    # filter_backends = [PlotsTaskControlFilter, ]
    filter_class = PlotsTaskControlFilter


class PlotsTaskResultViewSet(BaseModelViewSet):
    """
    用户秘钥
    """
    queryset = PlotsTaskResult.objects.all().order_by('-update_at')
    serializer_class = PlotsTaskResultSerializer
    # filter_backends = [PlotsTaskResultFilter, ]
    filter_class = PlotsTaskResultFilter
