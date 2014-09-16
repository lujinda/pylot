import socket
import select
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('0.0.0.0',1234))
server.listen(10)
server.setblocking(0)

epoll=select.epoll()
epoll.register(server.fileno(),select.EPOLLIN)
print 'server filno:',server.fileno()
try:
    connections={};requests={};responses={}
    while True:
        events=epoll.poll(1)
        for fileno,event in events:
            if fileno == server.fileno():
                connection,addr=server.accept()
                connFd=connection.fileno()
                print 'client fileno:',connFd
                connection.setblocking(0)
                epoll.register(connFd,select.EPOLLIN)
                connections[connFd]=connection
            elif event & select.EPOLLIN:
                requests[fileno]=connections[fileno].recv(1024).strip()
                print requests[fileno]
                epoll.modify(fileno,select.EPOLLOUT)

            elif event & select.EPOLLOUT:
                connections[fileno].send(requests[fileno]+'\n')
                epoll.modify(fileno,select.EPOLLIN)

            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]

finally:
    epoll.unregister(server.fileno())
    server.close()
            
            

