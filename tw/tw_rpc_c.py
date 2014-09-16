import sys
from twisted.spread import pb
from twisted.internet import reactor

def handle_err(reason):
    print 'a error occurred',reason
    reactor.stop()

def call_do(def_call_obj,cmd):
    return def_call_obj.callRemote("do",cmd)

def print_do(print_result):
    print print_result
    reactor.stop()

if __name__=="__main__":
    try:
        cmd=sys.argv[1:]
        if len(cmd)==0:raise IndexError
    except IndexError:
        print "need cmd"
        sys.exit(1)
    factory=pb.PBClientFactory()
    reactor.connectTCP("localhost",1234,factory)
    d=factory.getRootObject()
    d.addCallback(call_do,cmd)
    d.addCallback(print_do)
    d.addErrback(handle_err)
    reactor.run()
