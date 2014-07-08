from twisted.internet.defer import Deferred,succeed
from twisted.python import log
from twisted.application import internet,service
from twisted.internet.protocol import ClientFactory,ServerFactory,Protocol

class ProxyProtocol(Protocol):
    def connectionMade(self):
        d=self.factory.service.get_poem()
        d.addCallback(self.sendMsg)
        d.addBoth(lambda r:self.transport.loseConnection())
        
    
    def sendMsg(self,poem):
        self.transport.write(poem)
        log.msg("send %d bytes of poetry to %s"
                %(len(poem),self.transport.getPeer()))

class ProxyFactory(ServerFactory):
    protocol=ProxyProtocol
    def __init__(self,service):
        self.service=service
    

class clientProtocol(Protocol):
    poem=''
    def dataReceived(self,data):
        self.poem+=data

    def connectionLost(self,reason):
        self.factory.poem_finished(self.poem)

class clientFactory(ClientFactory):
    protocol=clientProtocol
    def __init__(self):
        self.deferred=Deferred()
    def poem_finished(self,poem):
        if self.deferred is not None:
            d,self.deferred = self.deferred,None
            d.callback(poem)

class ProxyService(service.Service):
    poem=None
    def __init__(self,host,port):
        self.host=host
        self.port=port


    def get_poem(self):
        if self.poem is not None:
            log.msg("Using cached poem.")
            return succeed(self.poem)
        log.msg("Fetching poem from server")
        factory=clientFactory()
        factory.deferred.addCallback(self.set_poem)
        from twisted.internet import reactor
        reactor.connectTCP(self.host,self.port,factory)
        return factory.deferred

    def set_poem(self,poem):
        self.poem=poem
        return poem


l_port=1238
r_port=1236
r_host="127.0.0.1"
top_service=service.MultiService()
proxy_service=ProxyService(r_host,r_port)
proxy_service.setServiceParent(top_service)
factory=ProxyFactory(proxy_service)
tcp_service=internet.TCPServer(l_port,factory,interface="localhost")
tcp_service.setServiceParent(top_service)
application=service.Application("poem")
top_service.setServiceParent(application)

