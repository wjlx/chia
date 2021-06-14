# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from celery import Celery


app = Celery('chia')
app.config_from_object('app.celeryconfig')
