#coding:utf8
from BeautifulSoup import BeautifulSoup as bs
import sys
import urllib2
from twisted.internet.defer import inlineCallbacks
from twisted.internet import defer,reactor 
from twisted.web.client import getPage,downloadPage
import parse

def parse_error(_,name):
    print name,"解析出错喽"

def parse_finished(_):
    print "视频均分析完成"
    fd.close()
    reactor.stop()
    

def readUrl():
    fd=open("list.txt")
    url_list=fd.readlines()
    fd.close()
    return url_list


class YouKu():
    hds={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (K    HTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}
    def __init__(self):
        pass
        
    def parse_url(self,result):
        result=result.decode("gbk")
        soup=bs(result)
        filename=soup("input",attrs={"name":"name"})[0]['value']
        fileurl=soup("input",attrs={"name":"inf"})[0]['value']
        fileurl=fileurl[:-1]
        
        return filename.encode("utf-8"),fileurl.encode("utf-8")
        
    def down_url(self,_):
        filename,fileurl=_
        filename=filename+'.flv'
        d=downloadPage(fileurl,filename)
        d.addCallback(parse.parseVedio,fd,filename)
        return d

@inlineCallbacks
def handler():
    dlist=[]
    count=0
    for url in readUrl():
        count+=1
        url=url.strip()
        d=getPage("http://www.flvcd.com/parse.php?format=&kw="+url)
        d.addCallback(youku.parse_url)
        d.addCallback(youku.down_url)
        d.addErrback(parse_error,url)
        dlist.append(d)

        if count%5==0:
            print "正在处理五个任务，其他任务稍等"
            ds=defer.DeferredList(dlist,consumeErrors=True)
            yield ds
            dlist
    ds=defer.DeferredList(dlist,consumeErrors=True)
    yield ds

        
if __name__=="__main__":
    youku=YouKu()
    fd=open("out.txt",'a+')
    d=handler()
    d.addBoth(parse_finished)


    reactor.run()
