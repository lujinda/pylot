import socket,sys

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1234))
s.shutdown(0)
print s.recv(1024),
s.sendall("abc")
