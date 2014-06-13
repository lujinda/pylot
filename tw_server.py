import optparse,os
import time

from twisted.internet.protocol import ServerFactory,Protocol

def parse_args():
    usage="""usage:%prog [options] poetry-file"""
    parser=optparse.OptionParser(usage)
    help="The port to listen to .Default to a random available port."
    parser.add_option('-p','--port',type="int",help=help)
    
    help="The interface to listen on.Default is localhost."
    parser.add_option('-i',"--iface",help=help,default="localhost")

    help="num-bytes"
    parser.add_option('-n',"--num-bytes",help=help,default=10)

    help="delay"
    parser.add_option('-d',"--delay",help=help,default=1)

    options,args=parser.parse_args()

    if len(args)!=1:
        parser.error("Provide exactly one poetry file.")

    poetry_file=args[0]

    if not os.path.exists(poetry_file):
        parser.error("No such file:%s"%poetry_file)
    return options,poetry_file
    

class PoetryProtocol(Protocol):
    
    def connectionMade(self):
        self.transport.write(self.factory.poem)
        self.transport.loseConnection()

class PoetryFactory(ServerFactory):
    protocol=PoetryProtocol
    
    def __init__(self,poem):
        self.poem=poem


def main():
    options,poetry_file=parse_args()
    poem=open(poetry_file).read()
    factory=PoetryFactory(poem)
    from twisted.internet import reactor
    port=reactor.listenTCP(options.port or 0,factory,interface=options.iface)
    port1=reactor.listenTCP(1235,factory,interface=options.iface)
    print "Serving %s on %s." %(poetry_file,port.getHost()) 

    reactor.run()

if __name__=="__main__":
    main()
