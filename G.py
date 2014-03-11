#coding:utf-8
import urllib,urllib2
url='http://translate.google.cn'
data={'sl':'zh-CN','tl':'en','js':'n','prev':'_t','hl':'zh-CN','ie':'UTF-8','text':'你好'}
data=urllib.urlencode(data)
header={'User-Agent':'chrome/28.0'}
req=urllib2.Request(url,data,header)
response=urllib2.urlopen(req).read()
response=unicode(response,'GBK').encode('UTF-8')
print response
