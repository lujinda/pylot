#!/usr/bin/python
#coding:utf-8
import re
import urllib2,urllib,socket
import sys
import os
import time
import threading
hds={'User-Agent':'chrome/28.0.1500.72',}
#proxy_h=urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})
#opener=urllib2.build_opener(proxy_h)
#urllib2.install_opener(opener)
def getHtml(url):
	page=urllib2.urlopen(urllib2.Request(url,None,hds)).read() #读取网页html源码
	return page
class getImgThread(threading.Thread):
    def __init__(self,imgUrl,fileName):
        threading.Thread.__init__(self)
        self.url=imgUrl
        self.fileName=fileName
    def run(self):
        mutex.acquire()
        print self.url
        mutex.release()
        urllib.urlretrieve(self.url,self.fileName)
if __name__ == '__main__':
    socket.setdefaulttimeout(10)
    Url=sys.argv[1]
    try:
		os.mkdir('img')
    except OSError,e:
		if e.errno == 17:#如果是文件已经存在，则不做任何操作
			pass
		else:			#如果是其他异常，则打印出异常，并退出程序 
			print e
			sys.exit()
    os.chdir('img')	
    page=getHtml(Url)
    r_img=re.compile(r"src=\"((http://|https://|)[\w/\.\-/]*\.(jpg|png|gif))\"",re.I)
    mutex=threading.Lock()
    threads=[]
    for URL in  r_img.findall(page):#做一个遍历
        try:
            if not URL[1]:	#当它是相对路径时
                URL=Url+'/'+URL[0]	#把它变成绝对路径
            else:
                URL=URL[0]	#直接是绝对路径
            fileName=URL.split('/')[-1]	#取文件名 
            threads.append(getImgThread(URL,fileName))

        except Exception,e:
            pass
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print 'End'
