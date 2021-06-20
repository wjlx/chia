# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from django_filters import FilterSet, NumberFilter, CharFilter

from .models import *


class UserKeyFilter(FilterSet):
    class Meta:
        model = UserKey
        fields = ('user_id', 'fingerprint')


class PlotsTaskFilter(FilterSet):
    user_key = CharFilter(field_name='user_key__fingerprint', label='用户秘钥')

    class Meta:
        model = PlotsTask
        fields = ('user_key',)


class PlotsTaskControlFilter(FilterSet):
    task_id = NumberFilter(field_name='plots_task__id', label='任务ID')
    user_key = CharFilter(field_name='plots_task__user_key__fingerprint', label='用户秘钥')

    class Meta:
        model = PlotsTaskControl
        fields = ('task_id', 'user_key')


class PlotsTaskResultFilter(FilterSet):
    task_id = NumberFilter(field_name='plots_task__id', label='任务ID')
    user_key = CharFilter(field_name='plots_task__user_key__fingerprint', label='用户秘钥')

    class Meta:
        model = PlotsTaskResult
        fields = ('task_id', 'user_key')
