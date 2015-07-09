#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:22:10
# Filename      : util.py
# Description   : 
import os
import uuid

def get_current_dir(_file):
    """获取当前文件所在的路径"""
    return os.path.dirname(os.path.abspath(_file))

def made_uuid():
    return uuid.uuid4().hex

def is_float(string):
    if string.count('.') == 1 and string.find('.') > 0:
        return string.replace('.', '').isdigit()

    return string.isdigit()

