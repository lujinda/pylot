#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:24:59
# Filename      : run.py
# Description   : 
from tornado.httpserver import HTTPServer
from tornado import options, ioloop
from tornado.options import options, define
from app import AdminApplication

define('port', type = int, default = 1235, help = 'listen port')

if __name__ == "__main__":
    options.parse_command_line()
    app = AdminApplication()
    http_server = HTTPServer(app, xheaders = True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

