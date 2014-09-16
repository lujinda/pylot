#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-03 14:36:06
# Filename        : t.py
# Description     : 

import gevent
from gevent.queue import Queue
from gevent.server import StreamServer

users = {}

def broadcast(msg):
    msg += '\n'
    for v in users.values():
        v.put(msg)

def reader(username, f):
    for l in f:
        msg = "%s> %s" % (username, l.strip())
        broadcast(msg)

def writer(q, sock):
    while True:
        msg = q.get()

        sock.sendall(msg)

def read_name(f, sock):
    while True:
        sock.sendall("Please enter your name: ")
        name = f.readline().strip()
        if name:
            if name in users:
                sock.sendall('That username is already taken.\n')
            else:
                return name

def handle(sock, client_addr):
    f = sock.makefile()

    name = read_name(f, sock)

    broadcast('## %s joined from %s.' % (name, client_addr[0]))

    q = Queue()
    users[name] = q

    try:
        r = gevent.spawn(reader, name, f)
        w = gevent.spawn(writer, q, sock)
        gevent.joinall([r, w])
    finally:
        del(users[name])
        broadcast('## %s left the chat.'%name)

if __name__ == "__main__":
    s = StreamServer(('0.0.0.0',1234), handle)
    s.serve_forever()


