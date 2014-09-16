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
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        req=urllib2.Request(login_url,
                urllib.urlencode(post_data),
                headers)
        result=urllib2.urlopen(req).read()
        self.parseLogin(result)
    def parseLogin(self,result):
        if result.startswith("登录成功"):
            self.logger.info("%s","登录成功")
            print "登录成功"
            self.getTime()
        else:
            self.logger.error("%s","登录失败")
            print "登录失败"

    def getTime(self):
        url="http://www.id666.com/member/index.asp"
        result=urllib2.urlopen(url).read()
        re_date=re.compile(r"<td>(\d{4}-\d{1,2}-\d{1,2})")
        endDate=re_date.findall(result)[1]
        self.setTime(endDate)

    def setTime(self,time):
        import shelve
        DB_PATH="/home/ljd/py/data.db"
        d=shelve.open(DB_PATH,"c")
        d['ID666空间到期']=time
        d.close()


if __name__=="__main__":
    options=parse_args()
    zhuji=ZhuJi()
    try:
        zhuji.login(options.user,options.pwd)
    except urllib2.URLError:
        zhuji.logger.error("网络连接出错")
        sys.exit(1)
    

