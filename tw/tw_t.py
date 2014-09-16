from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource

class Brow(Resource):
    def getChild(self,name,request):
        request.path=request.path[1:]
        print request.path
        return File("/tmp")

factory=Site(Brow())
reactor.listenTCP(1234,factory)
reactor.run()
