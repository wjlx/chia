# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import time
import os
import requests

from ws.plots import app
from ws.config import plots_config as cfg
from ws.config import api_config as api


header = {
    "Content-Type": "application/json"
}


@app.task(name="test")
def add(x, y):
    time.sleep(10)
    return x + y


# @app.tasks(name="plots")
def plots():
    cmd = f"{cfg['chia']} plots create"
    if 'size' in cfg:
        cmd += f" -k {cfg['size']}"
    if 'num' in cfg:
        cmd += f" -n {cfg['num']}"
    if 'num_threads' in cfg:
        cmd += f" -r {cfg['num_threads']}"
    if 'buffer' in cfg:
        cmd += f" -b {cfg['buffer']}"

    if 'farmer_public_key' not in cfg:
        raise ValueError("config.ini plots section must contain farmer_public_key")
    cmd += f" -f {cfg['farmer_public_key']}"

    if 'tmp_dir' not in cfg:
        raise ValueError("config.ini plots section must contain tmp_dir")
    cmd += f" -t {cfg['tmp_dir']}"

    if 'final_dir' not in cfg:
        raise ValueError("config.ini plots section must contain final_dir")
    cmd += f" -d {cfg['final_dir']}"

    sub = os.popen(cmd)
    for line in sub:
        line = line.strip()

    sub.close()
    return "done"


# @app.tasks(name="plots_test")
def plots_test(id):
    count = 10
    plots_task = 1
    for i in range(count):
        data = {
            "plots_task": plots_task,
            "total_block": count,
            "finished_block": i,
        }
        # url = api['url'] + api['plots_task_result'] + str(id)
        url = api['url'] + api['plots_task_result']
        # response = requests.post(url, data)
        # response = requests.put(url, data)
        response = requests.get(url, params={'id': id})
        print(response.json())
    return "done"


def get_user_key():
    import json
    cmd = f"{cfg['chia']} keys show"
    pipe = os.popen(cmd)
    msg = pipe.read()
    msg = msg.split("\n\n")
    msg = json.dumps(msg, indent=4)
    print(msg)
    pipe.close()


# plots_test('1')
get_user_key()
