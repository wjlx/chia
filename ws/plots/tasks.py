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
from ws.config import get_url
from ws.plots.fingerprint import create_update_fingerprint


header = {
    "Content-Type": "application/json"
}


def upload_plots_task():
    data = {}
    url = get_url("plots_task")
    ufp = create_update_fingerprint()
    data["user_key"] = ufp['id']
    keys = ["size", "num", "buffer", "num_threads", "buckets", "tmp_dir", "tmp2_dir", "final_dir"]
    data.update(dict(((k, cfg[k]) for k in keys if cfg[k])))
    response = requests.post(url, data).json()
    if response['status'] != "ok":
        raise ValueError("任务上传失败！")
    print("获取任务信息。")
    return response['data']


# @app.tasks(name="plots")
def upload_plots_task_result(task_id):
    url = get_url("plots_task_result")
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

    data = {
        "plots_task": task_id,
        "total_block": 0,
        "finished_block": 0,
        "message": "",
    }

    response = requests.put(url, data).json()
    if response['status'] != "ok":
        raise ValueError("上传任务初始化成功。")

    ptr_id = response['data']['id']

    sub = os.popen(cmd)
    for line in sub:
        data = {}
        data['plots_task'] = task_id
        data["total_block"] = 100
        data["finished_block"] = 10
        data["message"] = line
        # line = line.strip()
        response = requests.post(url + ptr_id, data).json()
        if response['status'] != "ok":
            raise ValueError("任务上传失败！")

    sub.close()
    print("任务执行完成！")
    return "done"


def upload_plots_task_result_test(task_id):
    url = get_url("plots_task_result")
    cmd = "ping www.baidu.com"

    data = {
        "plots_task": task_id,
        "total_block": 0,
        "finished_block": 0,
        "message": "",
    }

    response = requests.post(url, data).json()
    if response['status'] != "ok":
        raise ValueError("上传任务初始化成功。")

    ptr_id = response['data']['id']
    count = 0
    sub = os.popen(cmd)
    print("任务执行中......")
    for line in sub:
        count += 1
        data = {}
        data["plots_task"] = task_id
        data["total_block"] = 100
        data["finished_block"] = count
        data["message"] = line
        # line = line.strip()
        response = requests.put(url + str(ptr_id), data).json()
        if response['status'] != "ok":
            raise ValueError("任务上传失败！")

        if count >= 100:
            break

    sub.close()
    print("任务执行完成！")
    return "done"


def execute_plots_task():
    plots_task = upload_plots_task()
    # upload_plots_task_result(plots_task['id'])
    upload_plots_task_result_test(plots_task['id'])


execute_plots_task()
