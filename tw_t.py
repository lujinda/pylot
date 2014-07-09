from twisted.internet import defer
from twisted.web.client import getPage

hds={
        "":"Mozilla/11",
        }

def process(result):
    print result
    reactor.stop()

def callerr(_):
    reactor.stop()

d=getPage("http://localhost",headers=hds,timeout=1)
d.addCallback(process)
d.addErrback(callerr)

from twisted.internet import reactor
reactor.run()
