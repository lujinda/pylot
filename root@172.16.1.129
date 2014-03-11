#coding:utf8
"""
menu:放着编号和指令对应
"""
import socket
import sys
import thread
import re
import time
class client():
    def __init__(self):
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((sys.argv[1],4567))
            self.entryUser()
            print '登录成功!'
        except Exception,e:
            print e
            sys.exit()
        self.isOnLine=True
        thread.start_new_thread(self.isConn,())
        thread.start_new_thread(self.showChatRoom,())
        self.sendMess()
    def isConn(self):
        while True:
            if not self.sock.recv(1024).strip():
                print '与服务器之间的连接被断开'
                self.isOnLine=False
                sys.exit()
    def entryUser(self):
        self.username=raw_input('请输入您的网名:')
        while not self.username.strip():
            self.username=raw_input('请输入您的网名:')
        self.sock.sendall(self.username)
        self.sock.sendall('%s 已进入聊天室'%self.username)
    def showChatRoom(self):
        while self.isOnLine:
            data=self.sock.recv(2048)
            print data
    def sendMess(self):
        re_mess=re.compile(r'^\s{0,}$')
        while self.isOnLine:
            mess=raw_input('')
            mess="%s (%s):\n"%(self.username,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())) + mess +'\n%s' %('-'*len(mess))
            if not re_mess.match(mess):
                self.sock.sendall(mess)


if __name__=='__main__':
    startChat=client()
