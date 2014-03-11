#coding:utf8
import urllib2
import urllib
import re
r_gjc=re.compile(r'\"(.+?)\"')
gjc=urllib.quote(raw_input("请输入关键词:"))
url="http://suggestion.baidu.com/su?wd=%s&p=3&cb=window.bdsug.sug&from=superpage&t=1390365527548" %(gjc)

hds={
'Host':'suggestion.baidu.com',
'Referer':'http://www.baidu.com/'
'User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
}
req=urllib2.Request(url,None,hds)
page=unicode(urllib2.urlopen(req).read(),'GB2312').encode('utf8')
for x in r_gjc.findall(page):
    print x

