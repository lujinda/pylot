#!/usr/bin/env python
#coding:utf8

import atexit
import os

def clean():
    print "clean..."
atexit.register(clean)
os._exit(1)
