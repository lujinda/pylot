from twisted.internet.defer import Deferred
from twisted.internet.error import ConnectError
from twisted.internet.protocol import ClientFactory,ServerFactory,Protocol
from twisted.trial.unittest import TestCase

class PoetryServerProtocol(Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.poem)
        self.transport.loseConnection()

class PoetryServerFactory(ServerFactory):
    protocol=PoetryServerProtocol

    def __init__(self,poem):
        self.poem=poem

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
            d,self.deferred =self.deferred,None
            d.callback(poem)

    def clientConnectionFailed(self,connector,reason):
        if self.deferred is not None:
            d,self.deferred = self.deferred,None
            print "in err"
            d.errback(reason)

def get_poetry(host,port):
    from twisted.internet import reactor
    factory=PoetryClientFactory()
    reactor.connectTCP(host,port,factory)
    return factory.deferred

TEST_POEM="""\
This is a test!!!"""

class PoetryTestCase(TestCase):
    
    def setUp(self):
        factory=PoetryServerFactory(TEST_POEM)
        from twisted.internet import reactor
        self.port=reactor.listenTCP(0,factory,
                interface="127.0.0.1")
        self.portnum=self.port.getHost().port
        
    def tearDown(self):
        port,self.port=self.port,None
        return port.stopListening()
    
    def test_client(self):
        d=get_poetry("127.0.0.1",self.portnum)

        def got_poem(poem):
            print poem
            self.assertEquals(poem,TEST_POEM)
        d.addCallback(got_poem)
        return d
    
    def test_failure(self):
        d=get_poetry("127.0.0.1",0)
        print dir(self)
        return self.assertFailure(d,ConnectError)
