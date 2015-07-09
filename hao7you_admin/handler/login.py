#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 16:41:07
# Filename      : login.py
# Description   : 
from .public import ApiHandler
from db.account import create_default_account, check_account, lock_account
from util.error import Error
from util.enc import enc_password
from util.util import made_uuid
from util.email import send_email

class LoginHandler(ApiHandler):
    def get(self):
        create_default_account()
        self.render('login.html')

    def post(self):
        username = self.get_body_argument('username')
        password = enc_password(self.get_body_argument('password'))
        return_url = self.get_query_argument('return_url', '/')
        error = check_account(username, password)

        if error == Error.USER_NOT_EXIST:
            self.set_error('用户名和密码不匹配')
            return

        if error == Error.AUTH_FAILE:
            self.incr_login_counter(username)
            self.set_error('用户名和密码不匹配')
            return

        if error == Error.USER_LOCKED:
            self.set_error('用户已被锁定，请留意管理员邮箱内激活短信')
            return

        self.session['user'] = username
        self.session.save()

        self.set_result('return_url', return_url)
        self.clear_login_counter(username)

    def clear_login_counter(self, username):
        self.redis_db.delete(self.__counter_key(username))

    def __counter_key(self, username):
        return 'login:counter:' + username

    def incr_login_counter(self, username):
        counter = self.redis_db.incr(self.__counter_key(username))
        if counter == 3: # 如果错误到了3次，则锁定用户名, 并发送激活邮箱到管理员账号
            lock_account(username)
            self.send_active_email(username)

    def send_active_email(self, username):
        token = made_uuid()
        self.redis_db.set('account:active:%s' % (username,),
            token)
        active_url = self.full_host + '/active?username={username}&token={token}'.format(username = username, token = token)
        send_email('q8886888@qq.com', subject = "请激活您被锁定的账号",
                html = "<a href='{url}' target='_blank'>{url}</a>".format(url = active_url))

from .public import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.session.logout()
        self.redirect(self.get_login_url())

