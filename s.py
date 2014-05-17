from asyncore import dispatcher
from asynchat import async_chat
import asyncore
import socket

PORT=1234

class ChatSession(async_chat):
    def __init__(self,server,sock):
        async_chat.__init__(self,sock)
        self.set_terminator("\n")
        self.data=[]
        self.server=server
        self.push("Welcome to My Server!\n")

    def collect_incoming_data(self,data):
        self.data.append(data)

    def found_terminator(self):
        line="".join(self.data)
        self.data=[]
        self.server.broadcast(':'.join(map(str,self.addr))+": "+line)

    def handle_close(self):
        print "Close"
        async_chat.handle_close(self)
        self.server.disconnect(self)


class ChatServer(dispatcher):
    def __init__(self,port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("",port))
        self.listen(5)
        self.sessions=[]

    def disconnect(self,session):
        self.sessions.remove(session)

    def broadcast(self,line):
        for session in self.sessions:
            session.push(line+'\n')
    def handle_accept(self):
        conn,addr=self.accept()
        self.sessions.append(ChatSession(self,conn))

if __name__=="__main__":
    s=ChatServer(PORT)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
