# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

broker_url = 'redis://:123456@127.0.0.1:6379'
result_backend = 'redis://:123456@127.0.0.1:6379/0'
# result_backend = 'django-db'

timezone = 'Asia/Shanghai'

# imports = (
#     'app.task',
# )


task_serializer = 'msgpack'  # 任务序列化和反序列化使用msgpack方案
result_serializer = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
accept_content = ['json', 'msgpack']
task_result_expires = 60 * 60 * 24

enable_utc = True
