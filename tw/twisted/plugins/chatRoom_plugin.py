from zope.interface import implements
import sys
import os
sys.path.append(os.getcwd())
from tw_chatRoom_app import ChatFactory
from twisted.python import usage,log
from twisted.application import internet,service
from twisted.plugin import IPlugin

class Options(usage.Options):
    optParameters=[
            ['port','p',1234,'The port number to listen on.'],
            ['iface','i','0.0.0.0',"The interface to listen on."],
            ]

class ChatRoomMaker(object):
    implements(service.IServiceMaker,IPlugin)
    tapname="chatRoom"
    description="A ChatRoom service."
    options=Options

    def makeService(self,options):
        top_service=service.MultiService()
        tcp_service=internet.TCPServer(int(options['port']),
                ChatFactory,
                interface=options['iface'])
        tcp_service.setServiceParent(top_service)

        return top_service

service_maker=ChatRoomMaker()


