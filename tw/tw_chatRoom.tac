from twisted.application import internet,service
from tw_chatRoom_app import ChatFactory

port=1234
iface="0.0.0.0"
application=service.Application("chatRoom")
factory=ChatFactory()
tcp_service=internet.TCPServer(port,factory,
        interface=iface)
tcp_service.setServiceParent(application)

