#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 13:51:27
# Filename      : index.py
# Description   : 
from .public import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')

