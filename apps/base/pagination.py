# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from rest_framework.pagination import PageNumberPagination


class PageNumber(PageNumberPagination):
    """
    分页
    """
    page_size = 10
    page_size_query_param = "page_size"
