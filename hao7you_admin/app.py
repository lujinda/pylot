#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:18:36
# Filename      : app.py
# Description   : 
from tornado.web import Application
from handler import handlers
from util.util import get_current_dir
from lib.session import SessionManager
from db.db import session_db, redis_db
import os

class AdminApplication(Application):
    def __init__(self):
        settings = dict(
                debug = True,
                gzip = True,
                cookie_secret = 'ff6ab5a368a34990be505d52d0f8612e',
                template_path = os.path.join(get_current_dir(__file__),
                    'template'),
                static_path = os.path.join(get_current_dir(__file__),
                    'static'),
                login_url = '/login',
                )

        session_settings = dict(
                session_secret = '12sdflsdDfsde',
                session_timeout = 60000,
                store_db = session_db,
                )
        self.redis_db = redis_db

        self.session_manager = SessionManager(**session_settings)

        super(AdminApplication, self).__init__(handlers, **settings)

