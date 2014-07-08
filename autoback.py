#!/usr/bin/env python
import sys
import os
import time
from qiniu import conf,rs,io

PATH=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])))


class lsFile():
    def __init__(self):
        os.chdir(PATH)
        self.prefix=time.strftime("%Y%m%d",
                time.localtime())
        conf.ACCESS_KEY="BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm"
        conf.SECRET_KEY="WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs"

        policy=rs.PutPolicy("ljdpython")
        self.token=policy.token()

    def rFile(self,path="."):
        for f in os.listdir(path):
            if os.path.isdir(path+'/'+f):
                self.rFile(path+'/'+f)
            else:
                p=os.path.join(path,f)
                self.upFile(p,self.prefix+p[1:]) 

    def upFile(self,filepath,key):
        try:
            ret,err=io.put_file(self.token,key,filepath)
        except:
            pass


back=lsFile()
back.rFile()

