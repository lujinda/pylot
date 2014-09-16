from twisted.web import xmlrpc,server
from twisted.internet import reactor

class Example(xmlrpc.XMLRPC):
    def xmlrpc_echo(self,x):
        return x

    xmlrpc_echo.signature=[['string','string'],
            ['int','int'],
            ]

    def xmlrpc_add(self,a,b):
        return a+b

    xmlrpc_add.signature=[['string','string'],
            ['int','int'],
            ]

    xmlrpc_add.help="Add the arguments and return the sum"

r=Example()
xmlrpc.addIntrospection(r)
reactor.listenTCP(1236,server.Site(r))
reactor.run()

