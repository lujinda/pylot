import socket,sys
result=socket.getaddrinfo(sys.argv[1],None,0,socket.SOCK_STREAM)
for data in result:
    print data[4]
