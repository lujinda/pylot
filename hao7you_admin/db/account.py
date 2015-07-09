#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 16:52:24
# Filename      : account.py
# Description   : 
from .db import mongo_db
from util.enc import enc_password
from util.error import Error
account_doc_keys = ['username', 'password', 'last_login_time', 'last_login_ip', 'is_locked']

def user_is_exist(username):
    return bool(mongo_db.account.find_one({'username': username}))

def create_default_account():
    default_username = 'hao7you'
    if bool(mongo_db.account.find_one({})):
        return 
    account_data = dict().fromkeys(account_doc_keys, None)
    account_data['username'] = default_username
    account_data['password'] = enc_password('hao7you')
    mongo_db.account.insert(account_data)

def check_account(username, password):
    account = mongo_db.account.find_one({'username': username})
    if not account:
        return Error.USER_NOT_EXIST

    is_locked = account.get('is_locked', False)
    if is_locked:
        return Error.USER_LOCKED

    account = mongo_db.account.find_one({'username':username, 
        'password': password})
    if not account:
        return Error.AUTH_FAILE

    return None

def update_account(old_username, username, password):
    mongo_db.account.update({'username': old_username},
            {"$set": {'username': username,
                'password': password}})

def lock_account(username):
    mongo_db.account.update({'username': username},
            {"$set": {'is_locked': True}})

def unlock_account(username):
    mongo_db.account.update({'username': username},
            {"$set": {'is_locked': False}})

