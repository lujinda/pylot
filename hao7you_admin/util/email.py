#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-07 11:11:38
# Filename      : email.py
# Description   : 
from requests import post
from config import submail_config
from threading import Thread

def _send_email(to, subject, html):
    request_data = {
            'appid'     : submail_config.appid,
            'to'        : to,
            'html'      : html,
            'from'      : submail_config['from'],
            'signature' : submail_config.appkey,
            'subject'   : subject,
            }

    r = post(submail_config.send_url, data = request_data)
    print(r.json())

def send_email(to, subject, html):
    t = Thread(target = _send_email, 
            args = (to, subject, html))
    t.start()

