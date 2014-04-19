#coding:utf8
from ftplib import FTP as ftp
import sys
import os

class upFile:
    def __init__(self,localPath,ftpPath,host,user,pwd):
        self.conn=ftp(host)
        self.conn.login(user,pwd)
        try:
            self.conn.cwd(ftpPath) 
        except ftplib.error_perm,e:
            print '远程目录不存在或无权限访问!'
            sys.exit(1)
        self.localPath=localPath
        dirname=localPath.split('/')[-1] # 获取目录名,如果目录名最后有个/,如.a/，则表示不上传目录，如果没有/则表示上传目录
        if os.path.isdir(localPath): 
            os.chdir(localPath)
            print '+ '+dirname
            if dirname:
                self.enDir(dirname)
            self.walk()
        else:
            self.up(localPath) # 如果不是目录，直接上传文件

    def mkDir(self,path):
        try:
            self.conn.mkd(path)
        except ftplib.error_perm,e:
            print "mkdir error:",e
            sys.exit(1)

    def enDir(self,path):
        try:
            self.conn.cwd(path)
        except Exception,e:
            print e
            self.mkDir(path)
            self.enDir(path)

    def walk(self,level=1):
        for item in sorted(os.listdir(".")):
            if os.path.isdir(item):
                print '+ '*(level+1)+item
                os.chdir(item)
                self.enDir(item)
                self.walk(level+1) 
            else:
                print '| '*level+item
                self.up(item)
        self.conn.cwd("..")
        os.chdir("..")

    def up(self,path):
        fd=open(path,"rb")
        self.conn.storbinary("STOR %s"%os.path.basename(path),fd)
        fd.close()

def main():
    path=sys.argv[1]
    ftpPath=raw_input("请输入远程路径:")
    upFile(path,ftpPath,"127.0.0.1","ljd","zxc123")

if __name__=="__main__":
    main()
