#coding:utf8
import urllib
import urllib2
import cookielib
lgurl='http://linux.zj.cn/admin/index.php?action=login'
cookie_handler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36' }
postdata={'user':'ljd','pw':'linuxer',}
dt = urllib.urlencode(postdata)
req = urllib2.Request(lgurl,dt,headers)
opener = urllib2.build_opener(cookie_handler)
#urllib2.install_opener(opener) 这样就可以用urlopen(req)也能登录了
page=opener.open(req).read()
print page
