#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import logging
from django.http import HttpResponse, Http404
from rest_framework import exceptions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins

from .pagination import PageNumber

logger = logging.getLogger('chia')


class MixinView(object):
    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            if hasattr(self, 'get_authenticate_header'):
                auth_header = self.get_authenticate_header(getattr(self, 'request'))

                if auth_header:
                    exc.auth_header = auth_header
                else:
                    exc.status_code = 403
            return self.resp_fail(exc, 403)
        elif isinstance(exc, exceptions.PermissionDenied):
            exc.status_code = 406
            return self.resp_fail(exc, 406)
        elif isinstance(exc, exceptions.APIException):
            logger.warning(exc)
            return self.resp_fail(exc, 400)
        elif isinstance(exc, Http404):
            return self.resp_fail(exc, 404)
        logger.exception(exc)
        return self.resp_fail(exc, 500)

    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response, HttpResponse):
            response = self.update_data(response)
        return super(MixinView, self).finalize_response(request, response, *args, **kwargs)

    @staticmethod
    def resp_ok(data: [dict, list, str] = None, status_code=200):
        """正常封装"""
        result = {
            'status': 'ok',
            'code': status_code,
            'data': data if data is not None else 'ok'
        }
        return Response(result)

    @staticmethod
    def resp(data: [dict, list, str]):
        return Response(data)

    @staticmethod
    def resp_fail(msg: [str, exceptions.APIException] = 'fail', code=400, data=None):
        """错误封装"""
        if hasattr(msg, 'detail'):
            msg = ','.join(msg.detail) if isinstance(msg.detail, (tuple, list)) else msg.detail
        results = {
            'status': 'fail',
            "code": code,
            'msg': str(msg),
            'data': data
        }
        return Response(results)

    @classmethod
    def update_data(cls, response: HttpResponse):
        if not isinstance(getattr(response, 'data', {}), dict):
            response = cls.resp_ok(getattr(response, 'data'))
        if hasattr(response, 'data') and not ('status' in response.data and 'data' in response.data):
            response.data = {
                'status': getattr(response, 'status_text', 'ok').lower(),
                'code': response.status_code,
                'data': response.data
            }
        if hasattr(response, 'data') and response.data.get('status') not in ('ok', 'fail'):
            response.data['status'] = 'ok'
        return response

    @staticmethod
    def get_obj(queryset, **kwargs):
        return get_object_or_404(queryset, **kwargs)


class BaseModelViewSet(MixinView, ModelViewSet):
    pass


class BaseGenericViewSet(MixinView, GenericViewSet):
    serializer_class = serializers.Serializer


class BaseListViewSet(BaseGenericViewSet, mixins.ListModelMixin):
    pass


class BaseAPIView(MixinView, APIView):
    pass


# class BaseModelViewSet(ModelViewSet):
#     pagination_class = PageNumber
