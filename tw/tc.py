from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ClientFactory

class QuoteProtocol(Protocol):
    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        self.transport.write(self.factory.quote)

    def dataReceived(self,data):
        print 'Received quote:',data

        self.transport.loseConnection()

class QuoteClientFactory(ClientFactory):
    protocol=QuoteProtocol
    def __init__(self,quote):
        self.quote=quote


    def clientConnectionFaialed(self,connector,reason):
        print "Connection failed:",reason.getErrorMessage()
        maybeStopReactor()

    def clientConnectionLost(self,connector,reason):
        print "Connection lost:",reason.getErrorMessage()
        maybeStopReactor()

def maybeStopReactor():
    global quote_counter
    quote_counter -=1
    if not quote_counter:
        reactor.stop()

quotes=[
        "You snooze you lose",
        "The early bird gets the wrom",
        "Carpe diem",
        ]

quote_counter=len(quotes)
for quote in quotes:
    reactor.connectTCP("localhost",1234,QuoteClientFactory(quote))
reactor.run()

