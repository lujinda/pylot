#!/usr/bin/env python
import socket
import struct
import traceback
import time
host=''
port=1234

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

while 1:
    try:
        mess,addr=s.recvfrom(1024)
        secs=int(time.time())
        reply=struct.pack("!I",secs)
        s.sendto(reply,addr)
    except (KeyboardInterrupt,SystemExit):
        raise
    except:
        traceback.print_exc()
