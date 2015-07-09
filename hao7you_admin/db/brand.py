#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-07 15:28:39
# Filename      : brand.py
# Description   : 
from .db import psql_connect
from datetime import datetime
import json

@psql_connect
def xx_is_exist(_cur, column_name, column_value, table_name = 'brand'):
    return bool(_cur[table_name].find_one({column_name: column_value}))

def brand_name_is_exist(brand_name):
    return xx_is_exist('brand_name', brand_name)

def brand_alias_name_is_exist(brand_alias_name):
    return xx_is_exist('brand_alias_name', brand_alias_name)

def model_name_is_exist(model_name):
    return xx_is_exist('model_name', model_name, 'model')

@psql_connect
def add_brand(_cur, brand_name, brand_alias_name, brand_logo_url, brand_summary = None):
    brand_summary = brand_summary or None
    _cur.brand.insert({'brand_name': brand_name, 'brand_alias_name': brand_alias_name,
        'brand_logo_url': brand_logo_url, 'brand_summary': brand_summary, 'add_time': datetime.now()})

@psql_connect
def update_brand(_cur, brand_id, brand_name, brand_alias_name, brand_logo_url, brand_summary = None):
    _cur.brand.update({'brand_name': brand_name, 'brand_alias_name': brand_alias_name,
        'brand_logo_url': brand_logo_url, 'brand_summary': brand_summary},{'id': brand_id})

@psql_connect
def get_all_brand(_cur):
    return list(_cur.brand.find(order_by = 'add_time DESC'))

@psql_connect
def remove_brand(_cur, brand_id): return _cur.brand.remove({'id': brand_id})


@psql_connect
def get_brand(_cur, **condition):
    assert condition, 'must be has condition'
    return _cur.brand.find_one(condition)

@psql_connect
def add_model(_cur, brand_id, model_name, model_param):
    _cur.model.insert({'brand_id': brand_id, 'model_name': model_name,
        'param': json.dumps(model_param), 'add_time': datetime.now()})

@psql_connect
def get_all_model(_cur, brand_id):
    all_model = _cur.model.find({'brand_id': brand_id}, order_by="id DESC")
    return all_model

@psql_connect
def get_model_param(_cur, model_id):
    return _cur.model.find_one({'id': model_id}, ['param'])

@psql_connect
def remove_model(_cur, model_id):
    _cur.model.remove({'id': model_id})

