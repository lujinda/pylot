from asyncore import dispatcher
from asynchat import async_chat
import asyncore
import socket

import threading
import optparse

def parse_args():
    usage="""usage:%prog  [hostname:]port"""
    parser=optparse.OptionParser(usage)
    _,address=parser.parse_args()
    if not address:
        print parser.format_help()
        parser.exit()
    address=address[0]
    if ':' not in address:
        host="127.0.0.1"
        port=address
    else:
        host,port=address.split(':',1)

    return host,int(port)

class ChatSession(async_chat):
    def __init__(self,sock):
        async_chat.__init__(self,sock)
        self.data=[]
        self.set_terminator("\n")
        t=threading.Thread(target=self.sendMsg)
        t.setDaemon(True)
        t.start()

    def sendMsg(self):
        while True:
            self.push(raw_input()+'\n')
        
    def collect_incoming_data(self,data):
        self.data.append(data)

    def found_terminator(self):
        line=''.join(self.data)
        self.data=[]
        print line

    def handle_close(self):
        async_chat.handle_close(self)
    

class ChatClient(dispatcher):
    def __init__(self,host,port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.connect((host,port))

    def handle_connect(self):
        ChatSession(self)

    def handle_close(self):
        self.close()

        

        
if __name__=="__main__":
    host,port=parse_args()
    s=ChatClient(host,port)
    asyncore.loop()

