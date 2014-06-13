from asyncore import dispatcher
from asynchat import async_chat
import asyncore
import socket

class ChatServer(dispatcher):
    def __init__(self,port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("",port))
        self.listen(5)

    def handle_accpet(self):
        conn,addr=self.accept()
        print conn

if __name__=="__main__":
    s=ChatServer(1234)
    asyncore.loop()
