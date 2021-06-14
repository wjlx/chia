# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import time
from app import app


@app.task(name="test")
def add(x, y):
    time.sleep(10)
    return x + y
