import os
from time import sleep
import time
import sys
try:
    pid=os.fork()
    if pid>0:
        sys.exit(0)
except OSError,e:
    print e
os.chdir('/tmp')
fd=open("tmp.txt","w+")
for i in range(20):
    fd.write("%s\n"%time.asctime())
    fd.flush()
    sleep(2)
