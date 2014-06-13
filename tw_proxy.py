import optparse

from twisted.internet.defer import Deferred,succeed
from twisted.internet.protocol import ClientFactory,ServerFactory,Protocol

def parse_args():
    usage="""usage: %prog [option] [hostname]:port"""

    parser=optparse.OptionParser(usage)

    help="The port to listen on.Default to a random availabe port."
    parser.add_option('-p',"--port",type="int",help=help)

    help="The interface to listen on.Default is localhost."
    parser.add_option("--iface",help=help,default="localhost")

    options,args=parser.parse_args()

    if len(args)!=1:
        parser.error("Provied exactly one server addresss.")

    def parse_address(addr):
        if ':' not in addr:
            host="127.0.0.1"
            port=addr
        else:
            host,port=addr.split(':',1)

        if not port.isdigit():
            parser.error("Ports must be integers.")

        return host,int(port)
    
    return options,parse_address(args[0])

class PoetryClientProtocol(Protocol):
    poem=''

    def dataReceived(self,data):
        self.poem+=data

    def connectionLost(self,reason):
        self.factory.poem_finished(self.poem)

class PoetryClientFactory(ClientFactory):
    protocol=PoetryClientProtocol

    def __init__(self):
        self.deferred=Deferred()

    def poem_finished(self,poem):
        if self.deferred is not None:
            d,self.deferred=self.deferred,None
            print "in fin"
            d.callback(poem)

    def clientConnectionFailed(self,connector,reason):
        if self.deferred is not None:
            d,self.deferred =self.deferred,None
            d.errback(reason)
            

class PoetryProxyProtocol(Protocol):
    
    def connectionMade(self):
        d=self.factory.service.get_poem()
        print "in conn"
        d.addCallback(self.p)
        d.addCallback(self.transport.write)
        print "in conn2"
        d.addBoth(lambda r:self.transport.loseConnection())
    
    def p(self,_):
        print "in p"
        return _

class PoetryProxyFactory(ServerFactory):
    protocol=PoetryProxyProtocol

    def __init__(self,service):
        self.service=service

class ProxyService():
    poem=None
    def __init__(self,host,port):
        self.host=host
        self.port=port

    def get_poem(self):
        if self.poem is not None:
            print "Using cacched poem."
            return succeed(self.poem)

        print "Fetching poem from server."
        factory=PoetryClientFactory()
        factory.deferred.addCallback(self.set_poem)
        from twisted.internet import reactor
        reactor.connectTCP(self.host,self.port,factory)
        print "in get"
        return factory.deferred

    def set_poem(self,poem):
        self.poem=poem
        return poem



def main():
    options,server_addr=parse_args()
    service=ProxyService(*server_addr)
    factory=PoetryProxyFactory(service)
    from twisted.internet import reactor
    port=reactor.listenTCP(options.port or 0,factory,
            interface=options.iface)
    print "Proxying %s on %s." %(server_addr,port.getHost())

    reactor.run()


if __name__=="__main__":
    main()
