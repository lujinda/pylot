import time
from twisted.internet import reactor,threads
from twisted.internet.task import LoopingCall

def blockingApiCall(arg):
    return arg

def noblockingCall(arg):
    print arg

def printResult(result):
    time.sleep(1)
    print result

def finish():
    reactor.stop()


d=threads.deferToThread(blockingApiCall,"Goose")
d.addCallback(printResult)
LoopingCall(noblockingCall,"Duck").start(.25)

reactor.run()


