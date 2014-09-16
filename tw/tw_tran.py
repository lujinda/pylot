import optparse

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import NetstringReceiver

def parse_args():
    usage="""usage: %prog [options]"""

    parser=optparse.OptionParser(usage)

    help="The port to listen on. Default to a random available port."
    parser.add_option("-p","--port",type="int",help=help)

    options,args=parser.parse_args()

    if len(args)!=0:
        parser.error("Bad arguments.")

    return options

class TransformService():
    def comm(self,poem):
        return poem.lower()

class TransformProtocol(NetstringReceiver):
    def stringReceived(self,request):
        if '.' not in request:
            self.transport.loseConnection()
            return
        xform_name,poem=request.split('.',1)
        
        self.xformRequestReceived(xform_name,poem)

    def xformRequestReceived(self,xform_name,poem):
        meth=getattr(self,"xform_%s"%(xform_name),None)
        try:
            new_poem=meth(poem)
            self.sendString(new_poem+'\r\n')
        except:
            print "ok"
            pass
        finally:
            self.transport.loseConnection()

    def xform_comm(self,poem):
        return self.factory.service.comm(poem)
            
class TransformFactory(ServerFactory):
    protocol=TransformProtocol
    def __init__(self,service):
        self.service=service



def main():
    options=parse_args()
    service=TransformService()
    factory=TransformFactory(service)
    from twisted.internet import reactor
    
    port=reactor.listenTCP(options.port or 0,factory,
            interface="localhost")
    
    print "Serving transforms on %s."%(port.getHost())
    reactor.run()

if __name__=="__main__":
    main()
