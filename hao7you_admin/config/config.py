#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:44:11
# Filename      : config.py
# Description   : 
from util.util import get_current_dir
import os
import ConfigParser

cfg_path = os.path.join(get_current_dir(__file__), 'config.cfg')

if not os.path.exists(cfg_path):
    raise Exception('config.cfg not found')

CFG = ConfigParser.ConfigParser()
CFG.read(cfg_path)

class ConfigNotExist(Exception):
    pass


class Config(dict):
    def __init__(self, section):
        global CFG
        if not CFG.has_section(section):
            raise ConfigNotExist('Not had %s config' % (section, ))
        for key, value in CFG.items(section):
            self[key] = value

    def __getattr__(self, name):
        value = self[name]
        offset = value.find('#') # 让.cfg支持注解
        if offset == -1:
            return value
        else:
            return value[:offset]

