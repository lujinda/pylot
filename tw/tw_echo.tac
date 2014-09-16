from twisted.application import internet,service
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory,Protocol

class EchoProtocl(Protocol):
    def dataReceived(self,data):
        self.transport.write(data)

class EchoFactory(ServerFactory):
    protocol=EchoProtocl

application=service.Application("echo")
echoServer=internet.TCPServer(1234,EchoFactory())
echoServer.setServiceParent(application)

