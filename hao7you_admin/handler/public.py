#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:27:27
# Filename      : public.py
# Description   : 
from tornado.web import RequestHandler, HTTPError
from lib.session import Session
from functools import wraps
from config import urls_config

def authenticated(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        ignore_path = map(lambda x: x.strip(), urls_config.ignore_auth.split(';'))
        if self.request.path in ignore_path or self.is_authenticated():
            return method(self, *args, **kwargs)

        if self.request.method in ('GET', 'HEAD'):
            return_url = self.request.uri
            login_url = self.get_login_url() or '/login'
            self.redirect(login_url + '?return_url=' + return_url)
        else:
            raise HTTPError(403)

    return wrap

class PublicHandler(RequestHandler):
    def initialize(self):
        self.session = Session(self.application.session_manager, self)
        self.init_data()

    def init_data(self):
        pass

    @authenticated # tornado会在prepare()后检查一下_finished值，而redirect后会把_finished设置成True
    def prepare(self):
        self.method_before()
        
    def method_before(self):
        """在执行任何method前都会执行的"""
        pass

    @property
    def UA(self):
        return self.request.headers.get('User-Agent', '')

    def is_authenticated(self):
        return self.current_user

    @property
    def current_user(self):
        return self.session.get('user', None)

    @property
    def client_ip(self):
        return self.request.remote_ip

    @property
    def full_host(self):
        return self.request.protocol + '://' + self.request.host

    @property
    def redis_db(self):
        return self.application.redis_db

class BaseHandler(PublicHandler):
    pass

class ApiHandler(PublicHandler):
    def init_data(self):
        self._result_json = {'error': ''}
        self.is_send_result = False

    def set_error(self, error):
        self._result_json['error'] = error

    def set_result(self, name, value):
        self._result_json[name] = value

    def send_result_json(self):
        if (not self.is_send_result) and (not self._finished):
            self.write(self._result_json)
            self.is_send_result = True

    def finish(self, *args, **kwargs):
        if self.is_send_result == False and self.get_status() in (200, 304):
            self.send_result_json()

        return super(ApiHandler, self).finish(*args, **kwargs)

    def render(self, *args, **kwargs):
        assert self.is_send_result == False
        self.is_send_result = True

        return super(ApiHandler, self).render(*args, **kwargs)

    def get_true_args(self, *args):
        _result = []
        for arg in args:
            if isinstance(arg, (list, tuple)):
                arg_name, arg_args = arg[0], arg[1:]
            else:
                arg_name, arg_args = arg, []

            _result.append(getattr(self, 'get_' + arg_name)(*arg_args))
            if self.has_error():
                break

        for i in range(len(args) - len(_result)):
            _result.append(None)

        return _result

    def has_error(self):
        return bool(self._result_json.get('error'))

    def get_has_arguments(self, arg_name):
        """获取多个参数，并且值都要是有内容的"""
        args = self.get_arguments(arg_name) or []
        args = filter(lambda x: x.strip(), args)
        return args

