# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import time
from apps.plots import app


@app.task(name="test")
def add(x, y):
    time.sleep(10)
    return x + y
