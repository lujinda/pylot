#coding:utf8
import urllib
import urllib2
import re
import cookielib
import androidhelper
import xml.etree.ElementTree as et
droid=androidhelper.Android()

def showMess(mess):
    droid.makeToast(mess)

class ZhuJi():
    def __init__(self):
        self.hds={
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5    37.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
                }
        
        self.cj=cookielib.LWPCookieJar()
        cjProcess=urllib2.HTTPCookieProcessor(self.cj)
        opener=urllib2.build_opener(cjProcess,urllib2.HTTPHandler())
        urllib2.install_opener(opener)

    def login(self,user,pwd):
        login_url="http://www.id666.com/cmd/member/user_login.asp?cmd=login"
        post_data={
                "username":user,
                "password":pwd,
                }

        req=urllib2.Request(login_url,urllib.urlencode(post_data),
                self.hds)

        page=urllib2.urlopen(req)
        result=page.read()
        if result.startswith("登录成功"):
            pass
        else:
            showMess("登录失败")

    def onKey(self):
        url="http://www.id666.com/cmd/product/renew.asp?cmd=renew_auto"
        req=urllib2.Request(url,None,self.hds)
        page=urllib2.urlopen(req)
        root=et.fromstring(page.read().strip())
        state=root.find("cmdState").text
        mess='\n'.join((state,
                root.find("errMsg").text))

        showMess(mess)




zhuji=ZhuJi()
zhuji.login("q8886888@qq.com","zxc123")
zhuji.onKey()
        
