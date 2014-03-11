#!/usr/bin/python
#coding:utf-8
import re
import urllib2
import sys
import os
hds={'User-Agent':'chrome/28.0.1500.72',}
#proxy_h=urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})
"""如果需要账号密码认证，则需要使用proxy_a=urllib2.HTTPBasicAuthHandler().add_password('realm','host','username','password')，并把proxy_a传入urllib2.bulid_opener的第二个参数"""
#opener=urllib2.build_opener(proxy_h)
#urllib2.install_opener(opener)   
def getHtml(url):
    page=urllib2.urlopen(urllib2.Request(url,None,hds)).read() #读取网页html源码
    return page

def getImg(page):
    r_img=re.compile(r"src=\"((http://|https://|)[\w/\.\-/]*\.(jpg|png|gif))\"",re.I)#编译生成一个正则规则，匹配相对绝对，和多种图片格式
    for URL in  r_img.findall(page):#做一个遍历
        try:
            if not URL[1]:	#当它是相对路径时
                URL=Url+'/'+URL[0]	#把它变成绝对路径
            else:
                URL=URL[0]	#直接是绝对路径
            fileName=URL.split('/')[-1]	#取文件名 
            print URL
            img=urllib2.urlopen(urllib2.Request(URL,None,hds)).read()
            open(fileName,'w').write(img).close()

        except Exception,e:
            pass
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
    getImg(getHtml(Url))
