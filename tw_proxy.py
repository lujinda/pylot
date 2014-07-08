#coding:utf8
import optparse

from twisted.internet.defer import Deferred,succeed
from twisted.internet.protocol import ClientFactory,ServerFactory,Protocol

def parse_args():
    usage="""usage: %porg [options] [hostname:]port"""

    parser=optparse.OptionParser(usage)
    help="The port to listen on.Default to a random available port."
    parser.add_option("-p","--port",type="int",help=help)

    help="The interface to listen on. Default is localhost."
    parser.add_option("-i","--iface",help=help,default="localhost")

    options,args=parser.parse_args()

    if len(args)!=1:
        parser.error("Provied exactly one server address.")

    def parse_address(addr):
        if ':' not in addr:
            host="127.0.0.1"
            port=addr
        else:
            host,port=addr.split(":",1)

        if not port.isdigit():
            parser.error("Ports must be integers.")

        return host,int(port)
    
    return options,parse_address(args[0])


class ProxyServer():
    poem=None

    def __init__(self,host,port):
        self.host=host
        self.port=port

    def get_poem(self):
        if self.poem:
            print "Using cached poem"
            return succeed(self.poem)
        else:
            def canceler(d):
                print "Canceling poeme download."
                factory.deferred=None # 防止disconnect后，错误回调激活deferred,如果没有这行，在执行poemClientFactory,在poem_finished中，callback会被调用，会提示已被回调过了
                connector.disconnect()

            print "Fetching poem from server"
            deferred=Deferred(canceler) # 当Deferred没有被完全激活，会在cancel时，调用canceler
            deferred.addCallback(self.set_poem)
            factory=poemClientFactory(deferred)
            from twisted.internet import reactor
            connector=reactor.connectTCP(self.host,self.port,factory)
            return factory.deferred


    def set_poem(self,poem):
        self.poem=poem
        return poem

class ProxyProtocol(Protocol):
    def connectionMade(self):
        self.deferred=self.factory.server.get_poem()
        self.deferred.addCallback(self.transport.write)
        self.deferred.addBoth(lambda x:self.transport.loseConnection())

    def connectionLost(self,_):
        if self.deferred:
            d,self.deferred=self.deferred,None
            d.cancel()


class ProxyFactory(ServerFactory):
    protocol=ProxyProtocol
    def __init__(self,server):
        self.server=server

class ClientProtocol(Protocol):
    poem=''
    def dataReceived(self,data):
        self.poem+=data

    def connectionLost(self,_):
        self.factory.poem_finished(self.poem)

class poemClientFactory(ClientFactory):
    protocol=ClientProtocol
    def __init__(self,deferred):
        self.deferred=deferred

    def poem_finished(self,poem):
        if self.deferred:
            d,self.deferred=self.deferred,None
            d.callback(poem)
    
def main():
    options,address=parse_args()
    proxy=ProxyServer(*address)
    proxy_factory=ProxyFactory(proxy)
    from twisted.internet import reactor
    port=reactor.listenTCP(options.port or 0,
            proxy_factory,interface=options.iface)
    
    print "Proxying %s on %s."%(address,port.getHost())
    reactor.run()

if __name__=="__main__":
    main()
