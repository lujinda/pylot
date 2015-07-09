#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 15:36:32
# Filename      : manager.py
# Description   : 
from tornado.web import HTTPError
from .public import ApiHandler, authenticated
from db.account import check_account, update_account
from util.enc  import enc_password

ALL_MANAGER  = ('settings', 'account', 'logging')

class ManagerHandler(ApiHandler):
    def get(self, manager_obj):
        if manager_obj not in ALL_MANAGER:
            raise HTTPError(404)
        render = getattr(self, 'render_' + manager_obj)
        render()

    def render_settings(self):
        raise

    def render_account(self):
        self.render('manager/account.html')

    def render_logging(self):
        raise

    def put(self, manager_obj):
        assert manager_obj in ALL_MANAGER
        put_func = getattr(self, 'put_' + manager_obj)
        put_func()

    def put_account(self):
        old_username, old_password = self.get_true_args(('username', 'old_username'),
                ('password', 'old_password'))
        if self.has_error():
            return

        if check_account(old_username, old_password):
            self.set_error('旧的用户名密码不匹配')
            return

        new_username, new_password = self.get_true_args(('username', 'new_username'),
                ('password', 'new_password'))

        if self.has_error():
            return

        update_account(old_username, new_username, new_password)

    def get_username(self, key):
        _username = self.get_argument(key)
        if not _username: self.set_error('%s 字段不能为空' % (key, ))

        return _username

    def get_password(self, key):
        _password = self.get_argument(key)
        if not _password:
            self.set_error('%s 字段不能为空' % (key, ))
        
        return enc_password(_password)

