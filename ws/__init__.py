# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from pathlib import Path

from ws.plots import app as plots_app

BASE_DIR = Path(__file__).resolve().parent.parent

__all__ = ('plots_app', 'BASE_DIR')
