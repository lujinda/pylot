#coding:utf8
import socket
import select
import sys
import thread
import threading
import time
"""
server是用来和用户之间连接的，端口Sport
sockChat是用来发信息的,端口Cport
ClientList存的是用户名和IP的对应关系
ConList存放的是ip和端口的对应关系
"""
ClientList={}
ConList={}

class chatRoom():
    def __init__(self):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sockChat=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
     #   self.server.setblocking(False)
        host='0.0.0.0'
        Sport=4567
        Cport=4568
        try:
            self.server.bind((host,Sport))
            self.sockChat.bind((host,Cport))
            self.server.listen(50)
        except Exception,e:
            print e
            sys.exit()
        self.waitClient()

    def waitClient(self):
        while 1:
            conn,clientIp=self.server.accept()
            thread.start_new_thread(self.clientThread,(conn,clientIp,))
    def clientThread(self,conn,clientIp):
        username=self.changeName(conn,clientIp[0])
        #self.sendWelMess(username)
        #self.addConList(connAddr)
        isFirst=True
        while True:
            clientMess,chatAddr=self.sockChat.recvfrom(2048)
            self.sendMess(clientMess,chatAddr)
            isFirst=False
            self.addConList(chatAddr)
            #if not clientMess:
    def sendMess(self,mess,myAddr):
        for Ip in ConList:
            clientAddr=(Ip,ConList[Ip])
            if clientAddr != myAddr:
                self.sockChat.sendto(mess,clientAddr)
    def addConList(self,addr):
        ConList[addr[0]]=addr[1]
        """
        commands={
        'list_client':self.listClient,
        'change_name':self.changeName,
        }
        while 1:
            print 'wait com--'
            clientCom=conn.recv(1024).strip()
            print clientCom
            if clientCom in commands:
                commands[clientCom](conn,clientIp[0])
                
            else:
                self.exitClient(conn,clientIp[0])
                print 'bk'
                break
        """
 #----------------------------未聊天前的功能-----------------   
    def changeName(self,conn,ip):
        ClientList[ip]=conn.recv(1024).strip()
        return ClientList[ip]
#--------------------------------------------------"""
if __name__=='__main__':
    chatRoom()
