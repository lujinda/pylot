#!/usr/bin/env python

import os
import sys
import urllib
import urllib2
import re
import cookielib
import threading

tbHds={ 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Referer':'http://tieba.baidu.com/'

        }

class tieba:
    def __init__(self,fileUrl):
        self.qdPost={
        "ie":"utf-8",
        "kw":'',
        "tbs":'',
        }
        self.cj=cookielib.MozillaCookieJar(fileUrl)
        self.cj.load()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),
                urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        self.addQd()

    def addQd(self):
        url='http://tieba.baidu.com/sign/add'
        for kwUrl,kw in self.getKw():
            kwUrl="http://tieba.baidu.com" + kwUrl
            kw=unicode(kw,"gbk").encode("utf8")
            self.qdPost['kw']=kw
            self.qdPost['tbs']=self.getTbs("http://tieba.baidu.com/f?kw=%s&fr=index"%kw)
            qdData=urllib.urlencode(self.qdPost)
            req=urllib2.Request(url,qdData,tbHds)
            urllib2.urlopen(req)
            
    def getTbs(self,url):
        re_tbs=re.compile(r'PageData.tbs = \"(.+?)\"')
        page=urllib2.urlopen(url).read()
        return re_tbs.findall(page)[0]
    
    def getKw(self):
        likeUrl="http://tieba.baidu.com/f/like/mylike"
        page=urllib2.urlopen(likeUrl).read()
        re_kw=re.compile(r'<a href=\"(.+?)\" title=\"(.+?)\">')
        return re_kw.findall(page)

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
files=filter(lambda x:x.startswith("._cj_"),os.listdir('.'))
#for fileUrl in files:
#    threading.Thread(target=tieba,args=(fileUrl,)).start()
tieba("._cj_t.txt")


