#!/usr/bin/python
#coding:utf-8
import re
import urllib2
import sys
import os
from twisted.internet import defer,reactor
from twisted.web.client import getPage
hds={'User-Agent':'chrome/28.0.1500.72',}
def getImg(page):
    r_img=re.compile(r"src=\"((http://|https://|)[\w/\.\-/]*\.(jpg|png|gif))\"",re.I)#编译生成一个正则规则，匹配相对绝对，和多种图片格式

    urls=r_img.findall(page)
    dlist=[] # deferred列表

    def saveImg(img,filename):
        fd=open(filename,"wb")
        fd.write(img)
        fd.close()
        return filename

    def getError(_,filename):
        return defer.fail(filename)

    def getFinished(_):
        imgs=[]
        errors=[]
        map(lambda x:x[0] and imgs.append(x[1])==None or errors.append(x[1]),
                _)
        reactor.stop()
        print "图片下载完成."
        print "下载成功列表:"
        for i,img in enumerate(imgs):
            print img,
            if (i+1)%3==0:print 
        print "下载失败列表:"
        for i,error in enumerate(errors):
            print error.value,
            if (i+1)%3==0:print
        

    for URL in  urls:#做一个遍历
        if not URL[1]:	#当它是相对路径时
            URL=Url+'/'+URL[0]	#把它变成绝对路径
        else:
            URL=URL[0]	#直接是绝对路径
        fileName=URL.split('/')[-1]	#取文件名 
        print URL
        deferred=getPage(URL,timeout=1)
        dlist.append(deferred)
        deferred.addCallback(saveImg,fileName)
        deferred.addErrback(getError,fileName)
    d=defer.DeferredList(dlist,consumeErrors=True)
    d.addBoth(getFinished) # 当列表中的deferred都激活后，才会激活这个


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
