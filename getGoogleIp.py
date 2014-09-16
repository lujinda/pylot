#coding:utf8
import atexit
import optparse
from threading import Thread,RLock

OUTFILE="out.txt"
MAXTIMEOUT=300

def parse_args():
    usage="usage: %prog [options]"
    parser=optparse.OptionParser(usage)

    help="each ip number of tests"
    parser.add_option('-c','--count',help=help,default=3,type=int)

    options,_=parser.parse_args()

    return options
    

class testGoogle():
    ips=[]
    tlist=[]
    succIp=[]
    def getIp(self):
        url="http://www.legendsec.org/google.html"
        hds={"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}
        
        import urllib2
        req=urllib2.Request(url,None,hds)
        result=urllib2.urlopen(req).read()

        from bs4 import BeautifulSoup as bs
        import re
        root=bs(result)
        ip_list=root.findAll("td",text=re.compile(r"\d+\.\d+\.\d+\.\d+"))
        for ip in ip_list:
            self.ips.append(ip.a.text)

    def endThread(self):
        for t in self.tlist:
            t.join()
        
        self.saveto(OUTFILE)

    def saveto(self,path):
        try:
            fd=open(path,'w')
            if self.succIp:
                fd.write('|'.join(self.succIp))
                print "已将结果输出到%s"%(OUTFILE)
        except IOError:
            print '|'.join(self.succIp)
            print "保存到文件出错~"
        finally:
            fd.close()


    def connIp(self,options):
        import random
        atexit.register(self.endThread)
        self.r=RLock()
        while self.ips:
            now_ip=random.choice(self.ips)
            now_t=Thread(target=self.__connection,
                    args=(now_ip,options.count))
            now_t.setDaemon(True)
            self.tlist.append(now_t)
            self.ips.remove(now_ip)

            if len(self.tlist) == 5:
                for t in self.tlist:
                    t.start()
                for t in self.tlist:
                    t.join()
                self.tlist=[]
        
    def __connection(self,host,count):
        import socket
        import time
        socket.setdefaulttimeout(1)
        cost=0
        for port in (80,443):
            for i in range(count):
                start=time.time()
                s=socket.socket()
                try:
                    s.connect((host,port))
                    end=time.time()
                    cost+=(end-start)
                except:
                    break
                finally:
                    s.close()

        self.r.acquire()
        if cost:
            cost=cost*1000.0/count
            print u'connect to %s 平均用时%.2f ms'%(host,
                    cost)
            if cost<MAXTIMEOUT:
                self.succIp.append(host)
        else:
            print "connect to %s time out"%(host)
        self.r.release()

if __name__ == "__main__":
    options=parse_args()
    google=testGoogle()
    google.getIp()
    try:
        google.connIp(options)
    except KeyboardInterrupt:
        import sys
        sys.exit(0)

    
