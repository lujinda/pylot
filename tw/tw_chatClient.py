from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory,Protocol
from twisted.protocols.basic import LineReceiver

def parser_args():
    import optparse
    usage="Usage:%prog [host:]port"
    parser=optparse.OptionParser(usage)
    _,address=parser.parse_args()
    
    if not address:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host='127.0.0.1'
            port=addr
        else:
            host,port=addr.split(':',1)

        if not port.isdigit():
            parser.error("Ports must be integers.")

        return host,int(port)

    return parse_address(address[0])
    

class ChatProtocol(LineReceiver):
    delimiter=b'\n'
    def connectionMade(self):
        reactor.callInThread(self.sendToServer)

    def sendToServer(self):
        while self.transport.fileno()>0:
            self.sendLine(raw_input())

    def lineReceived(self,data):
        print data

    def connectionLost(self,reason):
        print 'bye'

    def connectionFailure(self,connector,reason):
        print reason.value

class ChatFactory(ClientFactory):
    protocol=ChatProtocol
    def clientConnectionFailed(self,connector,reason):
        print reason.value
        reactor.stop()

    def clientConnectionLost(self,connector,reason):
        reactor.stop()

host,port=parser_args()
chatFactory=ChatFactory()
reactor.connectTCP(host,port,chatFactory,timeout=3)
reactor.run()

