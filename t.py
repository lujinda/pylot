#coding:utf8
import socket
solist=[x for x in dir(socket) if x.startswith('SO_')]
solist.sort()
for x in iter(solist):
    print x

