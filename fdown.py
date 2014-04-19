#coding:utf8
"""
递归步骤如下:
    遍历目录下的所有元素，当查到是目录时，进入这个目录。再对这个新目录，进行遍历，每一个目录下的遍历结束后，则退到父目录。简单用以下图示:
    a--->
        b--->
            c.txt 
            c1.txt 当这里遍历完后退回前一层，即b目录，再去遍历b目录下的其他
        a.txt
        b.txt
    在本地上的操作是这样的：假如我要下载远程的py/a目录，则先递归建立py/a目录。然后再切到这个目录。当在ftp上切换目录时，本地也随之切换.
"""
from ftplib import FTP as ftp
import sys
import os

def mk(path): # 用来创建目录用的，如果目录已经存在则不执行什么
    try:
        os.mkdir(path)
    except OSError,e:
        if e.errno==17:
            pass
        else:
            sys.exit(1)
    
class downFile:
    def __init__(self,rootDir,host,user,pwd):
        self.conn=ftp(host)
        self.conn.login(user,pwd)
        try:
            self.conn.cwd(rootDir) 
        except ftplib.error_perm,e:
            print '远程目录不存在或无权限访问!'
            sys.exit(1)
        os.chdir(os.path.join("/tmp",rootDir))

    def down(self,path):
        fd=open(path,"wb")
        self.conn.retrbinary("RETR %s"%path,fd.write)
        fd.close()
    
    def walk(self,nextDir,path='.',level=0):
        for item in self.conn.nlst():
            if self.getType(item)=='d':
                print '+ '*(level+1)+item
                mk(item)
                os.chdir(item)
                self.conn.cwd(item)
                self.walk(item,os.path.join(path,item),level+1) # level用来控制输入样式。path 存着当前的完整目录
            else:
                self.down(item)
                print '| '*level+item," --->%s"%os.path.join(path,item)
            
        self.conn.cwd("..")
        os.chdir("..")
        
    def getType(self,path): # 只要能切换到path，则说明它是个目录，因为只有目录可以被切换。
        try:
            self.conn.cwd(path)
            self.conn.cwd("..")
            t='d'
        except:
            t='-'
        return t

    def run(self):
        self.walk(".")
        self.conn.quit()


def mkDir(path):
    if os.path.lexists(path): 
        pass
    else:
        mkDir(os.path.dirname(path)) # 一层一层往上退,只要没有存在，就递归下去。把它的父目录递归上去。
    mk(path)


def main():
    try:
        rootDir=raw_input("请输入你要下载的远程目录:")
        mkDir('%s'%os.path.join('/tmp',rootDir))
    except Exception,e:
        print e
        sys.exit(1)
    d=downFile(rootDir,"127.0.0.1","ljd","zxc123")
    d.run()

if __name__=="__main__":
    main()
