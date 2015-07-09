#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-07 13:32:33
# Filename      : active.py
# Description   : 
from .public import BaseHandler
from db.account import unlock_account
from tornado.web import HTTPError

class AccountActiveHandler(BaseHandler):
    def get(self):
        username = self.get_query_argument('username')
        token = self.get_query_argument('token')
        if self.auth_token(token, username):
            unlock_account(username)
            self.redirect(self.get_login_url())
        else:
            raise HTTPError(403)

    def auth_token(self, token, username):
        result = self.redis_db.get(self.__active_key(username)) == token
        if result:
            self.redis_db.delete(self.__active_key(username))

        return result

    def __active_key(self, username):
        return 'account:active:%s' % (username,)

