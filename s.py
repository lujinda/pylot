from getproxy import getProxyList
from twisted.web.client import getPage,HTTPClientFactory

import random

HTTPClientFactory().setURL('http://195.222.127.21:3128')

def f(result):
    print result

d=getPage("http://20140507.ip138.com/ic.asp")
d.addCallback(f)

from twisted.internet import reactor
reactor.run()
