#coding:utf8
import time
import socket
import struct
host="localhost"
port=1234
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto("",(host,port))

buf=s.recvfrom(2048)[0]
if len(buf)!=4:
    sys.exit(1)
secs=struct.unpack("!I",buf)[0] 
print time.ctime(int(secs))
