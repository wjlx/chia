# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import os
from configparser import ConfigParser

from ws import BASE_DIR


class Config(object):
    def __init__(self):
        self.cfg_path = os.path.join(BASE_DIR, 'ws/config/config.ini')
        self.__config = None

    @property
    def config(self):
        if self.__config is None:
            cfg = ConfigParser()
            cfg.read(self.cfg_path, encoding='utf-8')
            if "plots" not in cfg:
                raise ValueError("config.ini must contains 'plots' section !")
            if "api" not in cfg:
                raise ValueError("config.ini must contains 'api' section !")
            self.__config = cfg
        return self.__config


cfg = Config().config

plots_config = dict(cfg['plots'])
api_config = dict(cfg['api'])
