#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:36:32
# Filename      : db.py
# Description   : 
"""下面是psql的"""
from config import psql_config
from functools import wraps
import traceback
from .psql import PsqlConnection

db_conn = PsqlConnection(debug = True, **psql_config)

def psql_connect(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        _cur = db_conn.cursor()
        try:
            result = func(_cur, *args, **kwargs)
            return result
        except Exception as e:
            db_conn.rollback()
            raise e
        finally:
            db_conn.commit()

    return wrap

"""下面是mongodb的"""
import pymongo
import tmongo
from config import mongo_config

mongo_db = tmongo.TMongo(pymongo.Connection()[mongo_config.db_name])

"""下面是redis数据库相关的了"""
import redis
from config import redis_config

class RedisDb(object):
    def __init__(self, prefix, *args, **kwargs):
        self._prefix = prefix
        self._db = redis.Redis(*args, **kwargs)

    def __getattr__(self, func_name):
        if func_name.startswith('__'):
            return getattr(self._db, func_name)

        def _prefix_func(name, *args, **kwargs):
            key_name = self._prefix + name
            return getattr(self._db, func_name)(key_name, *args, **kwargs)

        return _prefix_func

session_db = RedisDb(**redis_config)
redis_db = RedisDb(**redis_config)

