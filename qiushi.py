#coding:utf8
import urllib2
from bs4 import BeautifulSoup as bs
hds={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}

url="http://www.qiushibaike.com"
req=urllib2.Request(url,None,hds)
result=urllib2.urlopen(req).read()

root=bs(result)
qiushi=root("div",attrs={"class":"article block untagged mb15"})

for item in qiushi:
    try:
        div_user=item("div",
            attrs={"class":"author clearfix"})[0]

        name=div_user.img['alt']
    except IndexError:
        name="匿名"
    div_content=item("div",
            attrs={"class":"content"})[0]
    time=div_content['title']
    content=div_content.text.strip()

    try:
        div_thumb=item("div",
                attrs={"class":"thumb"})[0]
        img=div_thumb.img['src']
    except IndexError:
        img=""

    print name,time,content,img
