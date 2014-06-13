import urllib
import urllib2
import re
import socket
socket.setdefaulttimeout(2)
url="http://www.zjccet.com/plus/chengji.php"
re_r=re.compile(r"<td>(.+?)</td>")
for i in range(1000000):
    postdata={"zkzh":"141391111%06d"%i}
    post=urllib.urlencode(postdata)
    print postdata
    req=urllib2.Request(url,post)
    try:
        page=urllib2.urlopen(req)
    except:
        continue
    page=page.read()
    for data in re_r.findall(page):
        print data.decode("gbk")
