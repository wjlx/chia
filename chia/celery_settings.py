# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""


CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
