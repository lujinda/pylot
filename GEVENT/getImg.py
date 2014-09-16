#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-12 06:50:34
# Filename        : getImg.py
# Description     : 
#import gevent.monky
#gevent.monky.patch_all()
import os
import urllib2
import sys
import re
import gevent
from gevent.queue import Queue

headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        }

def getUrl(page):
    re_img = re.compile(r"scr=[\"\']((http://|https://)[\w/\.\-/]*\.(jpg|png|gif))[\"\']", re.I)
    print re_img.findall(page)

def main(url):
    request = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(request).read()
    getUrl(page)

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError,e:
        print e
        sys.exit(1)

    main(url)
