#coding:utf8
import urllib2
import json
import re


import tempfile
htmlFile=tempfile.mkstemp()[1]+'.html'
fd=open(htmlFile,'w+')

LIST_URL="http://c.m.163.com/nc/article/list/T1350383429665/0-20.html"
result=urllib2.urlopen(LIST_URL).read()
result=json.loads(result)

list_page=result['T1350383429665']
for page in list_page:
    if re.search(u"轻松.*语音",page['title']):
        page['title'],page['url']


