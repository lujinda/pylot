#!/usr/bin/env python

import socket
import select

HEAD="HTTP/1.1 200 OK\r\nContent-Type: text/html\n\n"
responseBody="<b>Hello Word</b>\n\r\n"

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,)
serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
serversocket.setblocking(0)
serversocket.bind(('0.0.0.0',1236))
serversocket.listen(10240)

epoll=select.epoll()
epoll.register(serversocket.fileno(),select.EPOLLIN)

try:
    connections={}
    while True:
        events=epoll.poll(1)
        for fileno,event in events:
            if fileno==serversocket.fileno():
                connection,addr=serversocket.accept()
                connFd=connection.fileno()
                connections[connFd]=connection
                epoll.register(connFd,select.EPOLLIN)
            elif event & select.EPOLLIN:
                respon=connections[fileno].recv(1024).strip()
                epoll.modify(fileno,select.EPOLLOUT)
            elif event & select.EPOLLOUT:
                connections[fileno].sendall(HEAD)
                connections[fileno].sendall(responseBody)
                epoll.modify(fileno,select.EPOLLHUP)
                connections[fileno].close()

            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                del connections[fileno]
except Exception,e:
    print e
                
finally:
    epoll.unregister(serversocket.fileno())
    serversocket.close()



