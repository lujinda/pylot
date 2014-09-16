#coding:utf8
from twisted.internet import reactor,defer
from twisted.web.client import getPage,downloadPage
from twisted.internet.defer import inlineCallbacks

class open():
    def __init__(self,url):
        UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
        d=getPage(url=url,agent=UA)
        d.addCallback(self.get)
        d.addCallback(self.__down)
        d.addCallback(self.__end)
        d.addErrback(self.__error)

        reactor.run()

    def __end(self,_):
        print "下载任务结束！"
        reactor.stop()

    def __error(self,_):
        print _
        reactor.stop()

    def get(self,result):
        import re
        somedict={}
        re_down=re.compile(r"<td class=\"u-ctitle\">\s*(.+?)<a.+?>(.+?)<.+?downbtn.*?href=\'(.+?)\'",re.S)
        for item in re_down.findall(result): 
            item=map(lambda x:x.strip().decode("gbk").encode("utf8"),item)
            somedict[item.pop(0)]=item
        return somedict

    def __startDown(self,No,Name,Url):
        print "%s %s 开始下载!"%(No,Name)
        d=downloadPage(Url,No+Name+".mp4")
        return d
    
    def __endDown(self,_,No,Name,Url):
        print "%s %s 下载完成!"%(No,Name)

    def __downError(self,_,No,Name,Url):
        print "%s %s 下载失败!"%(No,Name)


    @inlineCallbacks
    def __down(self,result):
        dlist=[]
        count=0
        for No,value in result.items():
            Name,Url=value
            d=self.__startDown(No,Name,Url)
            d.addCallback(self.__endDown,No,Name,Url)
            d.addErrback(self.__downError,No,Name,Url)
            count+=1
            dlist.append(d)

            if count%5==0:
                print "正在下载五个视频，其他正在队列中!"
                ds=defer.DeferredList(dlist,consumeErrors=True)
                yield ds
                dlist=[]

        ds=defer.DeferredList(dlist,consumeErrors=True)
        yield ds
            
            
            
            
open("http://v.163.com/special/opencourse/algorithms.html")

