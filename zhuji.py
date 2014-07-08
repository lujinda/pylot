#coding:utf8
import urllib
import urllib2
import cookielib
import sys
import xml.etree.ElementTree as et
import re
import optparse
import logging

def parse_args():
    usage="""usage: %prog [options]"""

    parser=optparse.OptionParser(usage)
    help="username for zhujiwu"
    parser.add_option('-u','--user',help=help)
    help="password for zhujiwu"
    parser.add_option('-p','--pwd',help=help)

    options,_=parser.parse_args()
    if not(options.user or options.pwd):
        print parser.format_help()
        parser.exit()

    return  options
    
class ZhuJi():
    def __init__(self):
        self.hds={
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
                }
        self.cj=cookielib.LWPCookieJar()
        cjProcess=urllib2.HTTPCookieProcessor(self.cj)
        opener=urllib2.build_opener(cjProcess,urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        
        self.__conflog()
    
    def __conflog(self):
        log_file="/var/log/zhuji.log"
        self.logger=logging.getLogger("zhuji")
        handler=logging.FileHandler(log_file)
        formatter=logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)


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
            self.logger.info("%s","登录成功")
        else:
            self.logger.error("%s","登录失败")
            raise Exception

    def onKey(self):
        url="http://www.id666.com/cmd/product/renew.asp?cmd=renew_auto"
        req=urllib2.Request(url,None,self.hds)
        page=urllib2.urlopen(req)
        root=et.fromstring(page.read().strip())
        state=root.find("cmdState").text
        if re.search("成功".decode("utf8"),state):
            self.logger.info("%s",state)
            self.logger.info("%s",root.find("errMsg").text)
        else:
            self.logger.error("%s",state)
            self.logger.error("%s",root.find("errMsg").text)

if __name__=="__main__":
    options=parse_args()
    zhuji=ZhuJi()
    try:
        zhuji.login(options.user,options.pwd)
        zhuji.onKey()
    except urllib2.URLError:
        zhuji.logger.error("网络连接出错")
        sys.exit(1)
    

