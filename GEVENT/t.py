#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-11 08:39:47
# Filename        : t.py
# Description     : 

import gevent
from gevent.queue import Queue
from gevent.pool import Group

q = Queue(maxsize = 3)
group = Group()

def worker(n):
    print gevent.getcurrent()
    while not q.empty():
        task = q.get()
        print "Worker %s task %d" % (n, task)
        gevent.sleep(0)


def boss():
    for i in xrange(1,25):
        q.put(i)

g4 = gevent.spawn(boss)
g1 = gevent.spawn(worker,"lujinda")
g2 = gevent.spawn(worker,"lilanlan")
g3 = gevent.spawn(worker,"lll")
map(group.add,[g4,g2,g3,g1])
group.join()

