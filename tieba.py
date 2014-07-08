import urllib,urllib2,cookielib,re,json
import xml.etree.ElementTree as et
import sys

class LoginBd():
    def __init__(self):
        self.username,self.password=self.ReadInfo()
        self.InitCookie()
        self.SetNw()

    def SetNw(self):
        self.hds={
                "Host":"wappass.baidu.com",
                "Referer":"http://wappass.baidu.com/wp/api/login?v=1403866506485",
                "User-Agent":"Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; ZTE V955 Build/IMM76I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                }
        self.

    def InitCookie(self):
        cookiejar=cookielib.LWPCookieJar()
        self.c=cookiejar
        cookieSupport=urllib2.HTTPCookieProcessor(cookiejar)
        opener=urllib2.build_opener(cookieSupport,
                urllib2.HTTPHandler())
        urllib2.install_opener(opener)
    
    def GetCodeImg(self,url):
        pass

    def ReadInfo(self):
        tree=et.parse("baidu.xml")
        root=tree.getroot()
        return root.find("name").text,root.find("pass").text

class TieBd(LoginBd):
    def OneKeyQd(self):
        pass

if __name__=="__main__":
    tb=TieBd()
            

