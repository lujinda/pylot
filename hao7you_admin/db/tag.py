#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-09 18:32:45
# Filename      : tag.py
# Description   : 
from .db import psql_connect

@psql_connect
def add_tag(_cur, tag_name):
    _cur.tag.insert({'tag_name': tag_name})

@psql_connect
def update_tag(_cur, tag_id, tag_name):
    _cur.tag.update({'tag_name': tag_name}, {'id': tag_id})

@psql_connect
def remove_tag(_cur, tag_id):
    _cur.tag.remove({'id': tag_id})

@psql_connect
def tag_is_exist(_cur, tag_name):
    return _cur.tag.find_one({'tag_name': tag_name})

@psql_connect
def get_all_tag(_cur):
    return _cur.tag.find()

