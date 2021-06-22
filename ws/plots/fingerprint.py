# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import os

import requests

from ws.config import api_config as api
from ws.config import plots_config as cfg

header = {
    "Content-Type": "application/json"
}

fp_map = {
    "Fingerprint": "fingerprint",
    "Masterpublickey": "master_public_key",
    "Farmerpublickey": "farmer_public_key",
    "Poolpublickey": "pool_public_key",
    "Firstwalletaddress": "first_wallet_address",
}


def get_user():
    url = api['url'] + api['user']
    if not url.endswith('/'):
        url += "/"
    response = requests.get(url, params={'username': api['username']}).json()
    if response['status'] != "ok":
        raise ValueError(f"用户查询失败：{response['msg']}")
    data = response['data']
    if not data:
        raise ValueError("未查询到当前用户!")
    return data[0]


def parser_fingerprint(msg):
    data = []
    for fp in msg.split("\n\n")[1:]:
        d = []
        for line in fp.strip().split('\n'):
            k, v = line.replace(' ', '').split(':')
            d.append((fp_map[k.split("(")[0]], v))
        data.append(dict(d))
    return data


def get_fingerprint():
    cmd = f"{cfg['chia']} keys show"
    pipe = os.popen(cmd)
    msg = pipe.read()
    pipe.close()
    data = parser_fingerprint(msg)
    return data


def update_fingerprint():
    user = get_user()
    data = get_fingerprint()
    url = api['url'] + api['user_key']
    if not url.endswith('/'):
        url += "/"
    for d in data:
        d['user'] = user['id']
        if cfg['fingerprint'] == d['fingerprint']:
            response = requests.get(url, params={'fingerprint': d['fingerprint']}).json()
            if response['status'] != "ok":
                raise ValueError(f"从服务器获取用户秘钥错误，错误信息：{response['msg']}")
            rd = response['data']
            if len(rd) > 1:
                raise ValueError("从服务器查询的用户秘钥不唯一！")
            if rd:
                uk = rd[0]
                if uk['fingerprint'] != d['fingerprint']:
                    raise ValueError("当前用户秘钥与从服务器查询秘钥不匹配，查询错误！")
                url += str(uk['id'])
                response = requests.put(url, d).json()
                if response['status'] != "ok":
                    raise ValueError("更新用户秘钥失败！")
            else:
                response = requests.post(url, d).json()
                if response['status'] != "ok":
                    raise ValueError("创建用户秘钥失败！")


# get_user()
# get_fingerprint()
update_fingerprint()
