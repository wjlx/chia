# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from .config import plots_config, api_config


def get_url(name):
    url = api_config['url'] + api_config[name]
    if not url.endswith('/'):
        url += "/"
    return url


__all__ = ('plots_config', 'api_config', 'get_url')
