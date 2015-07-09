#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:50:36
# Filename      : __init__.py
# Description   : 
from .config import Config
config_list = ['redis', 'mongo', 'urls', 'submail', 'psql']

for config_name in config_list:
    locals()[config_name + '_config'] = Config(config_name)

