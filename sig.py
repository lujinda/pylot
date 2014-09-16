#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-26 16:31:45
# Filename        : sig.py
# Description     : 
import signal
import sys

def in_end(signum,_):
    print "bye"
    sys.exit(0)


if __name__=="__main__":
    signal.signal(signal.SIGINT,in_end)
    signal.signal(signal.SIGTERM,in_end)

    while True:
        pass


