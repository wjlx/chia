# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chia.settings')  # 设置django环境

app = Celery('chia')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('app.celeryconfig')
app.autodiscover_tasks()
