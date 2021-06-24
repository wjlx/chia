# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    :

:Content:

执行命令：
./chia plots create -k 32 -n 1 -r 4 -b 6750 \
                    -f b70a8bdc877ee1e2f0e4874e46bc6504d3018f65a7cc7aae140ce3db7b56af96b861aafd0316627d3af4cc226b31df67 \
                    -t /Users/wjl/data/chia/tmp \
                    -d /Users/wjl/data/chia/final \
执行结果：
2021-06-20T23:28:31.237  chia.plotting.create_plots       : INFO     Creating 1 plots of size 32, pool public key:  a1dae0bbe4ee28c6eb99bb5ae989496fbd039984918621b038f9c25a9178dbabc02a7b4181522025f2fce0f05739c053 farmer public key: b70a8bdc877ee1e2f0e4874e46bc6504d3018f65a7cc7aae140ce3db7b56af96b861aafd0316627d3af4cc226b31df67
2021-06-20T23:28:31.247  chia.plotting.create_plots       : INFO     Memo: a1dae0bbe4ee28c6eb99bb5ae989496fbd039984918621b038f9c25a9178dbabc02a7b4181522025f2fce0f05739c053b70a8bdc877ee1e2f0e4874e46bc6504d3018f65a7cc7aae140ce3db7b56af96b861aafd0316627d3af4cc226b31df6717cc918c2daa30d628b2ae6ba604cb06d0f2c32a571af7d48c10285b2b0fcea8
2021-06-20T23:28:31.248  chia.plotting.create_plots       : INFO     Adding directory /Users/wjl/data/chia/final to harvester for farming
2021-06-20T23:28:31.313  chia.plotting.create_plots       : INFO     Starting plot 1/1

Starting plotting progress into temporary dirs: /Users/wjl/data/chia/tmp and /Users/wjl/data/chia/tmp
ID: 94172a2bfc25cb42dd49db5ca82d9df007a028aa21f0e025ef9d0db8b6069407
Plot size is: 32
Buffer size is: 6750MiB
Using 128 buckets
Using 4 threads of stripe size 65536

Starting phase 1/4: Forward Propagation into tmp files... Sun Jun 20 23:28:31 2021
Computing table 1


F1 complete, time: 212.12 seconds. CPU (107.22%) Sun Jun 20 23:32:03 2021
Computing table 2
    Bucket 0 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
    Bucket 1 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
    Bucket 2 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
    Bucket 3 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
    Bucket 4 uniform sort. Ram: 6.525GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
    Bucket 5 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
    Bucket 6 uniform sort. Ram: 6.525GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
    Bucket 7 uniform sort. Ram: 6.525GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
"""

import os

import requests

from ws.config import get_url
from ws.config import plots_config as cfg
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


def finished_block_parse(line):
    finished_block = 0
    line = line.strip()
    if line.startswith("Bucket"):
        finished_block = int(line.split(" ")[1])
    return finished_block


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

    ptr = response['data']
    ptr_id = ptr['id']

    sub = os.popen(cmd)
    for line in sub:
        data = dict()
        data['plots_task'] = task_id
        data["total_block"] = 100
        data["finished_block"] = finished_block_parse(line)
        data["message"] = ptr["message"] + "\n" + line
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
