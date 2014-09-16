#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-29 11:07:53
# Filename        : qjvpn.py
# Description     : 

import cookielib
import urllib2
import urllib

def parser_args():
    import optparse
    usage = "Usage:%porg option"
    parser = optparse.OptionParser(usage)
    help = "usernamae for qivpn.net"
    parser.add_option('-u','--user',help = help)

    help = "password for qivpn.net"
    parser.add_option('-p','--pwd',help = help)

    options,_ = parser.parse_args()
    if not (options.user or options.pwd):
        print parser.format_help()
        parser.exit()

    return options


class QjVpn(object):
    hds = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            }
    def __init__(self):
        self.cj = cookielib.LWPCookieJar()
        cj_process = urllib2.HTTPCookieProcessor(self.cj)
        opener = urllib2.build_opener(cj_process)
        urllib2.install_opener(opener)


    def login(self,username,password):
        login_url = "http://www.qjvpn.net/user/checklogin.php"
        login_post = {
                'username':username,
                'password':password,
                'from':'',
                }
        
        self.__send_request(login_url,login_post,self.hds)

    def __send_request(self,url,data = None,hds = None):
        request = urllib2.Request(url,urllib.urlencode(data),
                hds)
        response = urllib2.urlopen(request)
        return response

    def sign(self):
        sign_url = "http://www.qjvpn.net/ajax2.php?fun=sign"
        sign_post = {
                'fun':'sign',
                }
        return_code = int(self.__send_request(sign_url,
            sign_post,self.hds).read())

        return return_code

if __name__=="__main__":
    options =parser_args()
    qjvpn = QjVpn()
    qjvpn.login(options.user,options.pwd)
    if qjvpn.sign() == 0:
        print '签到失败'
    else:
        print "签到成功"
    

    
