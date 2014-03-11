#client ubuntu
import socket
address=('172.16.1.128',1234)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    msg=raw_input()
    s.sendto(msg,address)
s.close()
