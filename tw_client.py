import optparse
import random
import sys

from twisted.internet import defer
from twisted.internet.protocol import Protocol,ClientFactory

def  parse_args():
    usage="""usage:%prog [hostname:]port"""
    parser=optparse.OptionParser(usage)

    _,addresses=parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host="127.0.0.1"
            port=addr
        else:
            host,port=addr.split(":",1)

        if not port.isdigit():
            parser.error("Ports must be intergers!")

        return host,int(port)
    
    return map(parse_address,addresses)

class PoetryProtocol(Protocol):
    poem=[]
    def dataReceived(self,data):
        self.poem.append(data)

    def connectionLost(self,reason):
        poem=''.join(self.poem)
        self.factory.poem_finished(poem)

class PoetryClientFactory(ClientFactory):
    protocol=PoetryProtocol
    def __init__(self,deferred):
        self.deferred=deferred

    def poem_finished(self,poem):
        if self.deferred is not None:
            d,self.deferred=self.deferred,None
            d.callback(poem)

    def clientConnectionFailed(self,connector,reason):
        if self.deferred is not None:
            d,self.deferred=self.deferred,None
            d.errback(reason)

def get_poetry(host,port):
    d=defer.Deferred()
    from twisted.internet import reactor
    factory=PoetryClientFactory(d)
    reactor.connectTCP(host,port,factory)
    return d

class GibberishError(Exception):pass
class CannotCummingsify(Exception):pass

def cummingsify(poem):
    def success():
        return poem.lower()
    def gibberish():
        raise GibberishError()
    def bug():
        raise CannotCummingsify(poem)
    
    return random.choice([success,gibberish,bug])()

def poetry_main():
    addressess=parse_args()
    poems=[]
    errors=[]
    
    def got_poetry(poem):
        print poem
        poems.append(poem)

    def poem_failed(err):
        print >>sys.stderr,"The poem download failed."
        errors.append(err)

    def poem_done(_):
        if len(poems)+len(errors)==len(addressess):
            from twisted.internet import reactor
            reactor.stop()

    def cummingsify_failed(err):
        if err.check(CannotCummingsify):
            print "Cummingsify failed!"
            return err.value.args[0]
        return err


    for address in addressess:
        host,port=address
        d=get_poetry(host,port)
        d.addCallback(cummingsify)
        d.addErrback(cummingsify_failed)
        d.addCallbacks(got_poetry,poem_failed)
        d.addBoth(poem_done)
    
    from twisted.internet import reactor
    reactor.run()

poetry_main()


        


