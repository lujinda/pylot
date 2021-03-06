#!/usr/bin/python
#coding:utf-8
import re
import urllib2
import sys
import os
from twisted.internet import defer,reactor
from twisted.web.client import getPage
hds={'User-Agent':'chrome/28.0.1500.72',}
def getHtml(url):
    page=urllib2.urlopen(urllib2.Request(url,None,hds)).read() #读取网页html源码
    return page

def getImg(page):
    r_img=re.compile(r"src=\"((http://|https://|)[\w/\.\-/]*\.(jpg|png|gif))\"",re.I)#编译生成一个正则规则，匹配相对绝对，和多种图片格式

    imgs=[]
    errors=[]
    urls=r_img.findall(page)

    def saveImg(img,filename):
        fd=open(filename,"wb")
        fd.write(img)
        fd.close()
        imgs.append(filename)

    def getError(_):
        print _
        errors.append(_)

    def getFinished(_):
        if len(errors)+len(imgs)==len(urls):
            reactor.stop()

    for URL in  urls:#做一个遍历
        if not URL[1]:	#当它是相对路径时
            URL=Url+'/'+URL[0]	#把它变成绝对路径
        else:
            URL=URL[0]	#直接是绝对路径
        fileName=URL.split('/')[-1]	#取文件名 
        print URL
        deferred=getPage(URL)
        deferred.addCallback(saveImg,fileName)
        deferred.addErrback(getError)
        deferred.addBoth(getFinished)


if __name__ == '__main__':
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
    d=getPage(Url)
    d.addCallback(getImg)
    reactor.run()
