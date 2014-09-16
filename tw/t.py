from twisted.internet import protocol,reactor

class Echo(protocol.Protocol):
    def dataReceived(self,data):
        self.transport.write(data)

class EchoFactory(protocol.ServerFactory):
    protocol=Echo

reactor.listenTCP(1234,EchoFactory())
reactor.run()
