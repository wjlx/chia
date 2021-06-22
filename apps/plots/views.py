# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from django.contrib.auth import hashers
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from apps.base.views import BaseModelViewSet
from .filters import *
from .serializers import *

DEFAULT_RETURN_DATA = {
    "status": 'ok',
    "version": '0.0.1'
}


class UserView(BaseModelViewSet):
    """
    用户注册
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        # return User.objects.filter(username=self.request.user)
        return User.objects.filter(username=username)

    def create(self, request, *args, **kwargs):
        params = {}
        data = request.data
        password = data.get("password", None)
        if password:
            password = hashers.make_password(password)
        data['password'] = password
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = True
        data = request.data
        instance = self.get_object()
        password = data.get("password", None)
        if password:
            password = hashers.make_password(password)
            data['password'] = password
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return serializer.save(owner=request.user)


class UserKeyViewSet(BaseModelViewSet):
    """
    用户秘钥
    """
    # queryset = UserKey.objects.all().order_by('-update_at')
    serializer_class = UserKeySerializer
    # filter_backends = [UserKeyFilter]
    filter_class = UserKeyFilter

    def get_queryset(self):
        user_key_id = self.request.query_params.get("id", None)
        user_id = self.request.query_params.get("user_id", None)
        fingerprint = self.request.query_params.get("fingerprint", None)
        queryset = UserKey.objects.all()
        if user_key_id:
            queryset = queryset.filter(id=user_key_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if fingerprint:
            queryset = queryset.filter(fingerprint=fingerprint)
        return queryset.order_by('-update_at')


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
    # queryset = PlotsTaskResult.objects.all().order_by('-update_at')
    serializer_class = PlotsTaskResultSerializer
    # filter_backends = [PlotsTaskResultFilter, ]
    filter_class = PlotsTaskResultFilter

    def get_queryset(self):
        task_id = self.request.query_params.get("id", None)
        queryset = PlotsTaskResult.objects.filter(id=task_id)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     # return_data = DEFAULT_RETURN_DATA.copy()
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     # return_data['results'] = serializer.data
    #     return Response(serializer.data)
    #
    # def test(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data[0])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(DEFAULT_RETURN_DATA, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(DEFAULT_RETURN_DATA, status=status.HTTP_206_PARTIAL_CONTENT)
