#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-08 13:01:19
# Filename      : test.py
# Description   : 
from psql import PsqlConnection

conn = PsqlConnection(user = 'ljd',
        password = 'zxc123', debug = True)

cur = conn.cursor()
cur.defa.update({'sdf': 'sdf'}, {'password': '123', "$or": [{'username': 'ljd'}, {'email': 'q88'}]})

conn.brand.find({'brand_name': u'小米'})
conn.brand.find({'age': {'$lt': 10}})
#conn.brand.find({'$or': [{'name': 'ljd', 'sex': 'boy'}, {'age': {'$lt': 10}}, {'no': {'$in': [1, 2, 3, 4]}}]})

print(conn.brand.find_one({"id": {'$lt': 1}}, ['id']))
#conn.brand.insert([{u'name': u'你好'}, {'name': '哈哈'}])
#conn.brand.update({'brand_name': '鲁'}, {'brand_name': '小米'})

#conn.brand.remove({'brand_name': '小米'})
