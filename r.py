from rarfile import RarFile
from rarfile import BadRarFile
from rarfile import PasswordRequired
import os
import threading
lock=threading.RLock()
rar=RarFile("/home/ljd/1.rar")
filename=rar.namelist()[0]
def loopkey(start,stop):
    for x in xrange(start,stop):
        try:
            rar.setpassword(str(x))
            rar.read(filename)
            print x   
            os._exit(0)
        except BadRarFile,PasswordRequired:
            pass
def looprange(n):
    data=range(0,n+1,n/100)
    return [(value,data[index+1]) for index,value in enumerate(data[:-1])]
data=looprange(1000000000)
print data
for x,y in data:
    threading.Thread(target=loopkey,args=(x,y)).start()
