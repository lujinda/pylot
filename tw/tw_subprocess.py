import sys
from twisted.internet import protocol,utils,reactor
from twisted.protocols.basic import LineReceiver
from twisted.python import log

class RunCommand(LineReceiver):
    delimiter='\n'
    def lineReceived(self,line):
        log.msg("Man pages requested for:%s"%(line,))
        commands=line.strip().split(" ")
        output=utils.getProcessOutput("man",commands,errortoo=True)
        output.addCallback(self.writeSuccessResponse)

    def writeSuccessResponse(self,result):
        self.transport.write(result)
        self.transport.loseConnection()

class RunCommandFactory(protocol.ServerFactory):
    protocol=RunCommand

log.startLogging(sys.stdout)
reactor.listenTCP(1234,RunCommandFactory())
reactor.run()




