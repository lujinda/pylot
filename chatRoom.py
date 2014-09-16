#coding:utf8
from asyncore import dispatcher
from asynchat import async_chat
import asyncore
import socket


class EndSession(Exception):pass

class CommandHandler:
    def handle(self,session,line):
        if not line.strip():return 
        parts=line.split(' ',1)
        cmd=parts[0].strip()
        try:
            if cmd[0]!='/':
                cmd="/say"
                line=line.strip()
            else:
                line=parts[1].strip()
        except IndexError:
            line=""
        finally:
            cmd=cmd[1:].strip()
        
        meth=getattr(self,"do_"+cmd,None)
        try:
            meth(session,line)
        except TypeError:
            self.unknow(session,cmd)

    def unknow(self,session,cmd):
        session.push("%s: unknow command!\n"%cmd)

class Room(CommandHandler): # 每次登录时会执行一下(LoginRoom)，新建一个聊天室或刚启动时会创建一个(ChatRoom)
    def __init__(self,server,name=""):
        self.server=server # server永远是指ChatServer
        self.roomName=name 
        self.sessions=[]    # 因为每次创建一个新的聊天室时，都会执行一下，这样的话不同聊天室之间的实例的数据其实是不共享的
    
    def add(self,session):
        self.sessions.append(session)

    def remove(self,session):
        self.sessions.remove(session)

    def broadcast(self,line):
        for session in self.sessions:
            session.push(line)
    
    def do_list(self,session,line):
        session.push("list for ChatRoom:\n")
        for roomName in self.server.rooms:
            session.push(roomName+'\n')
    def do_logout(self,session,line):
        raise EndSession

class LoginRoom(Room):
    def add(self,session):
        Room.add(self,session)
        self.broadcast("Welcome to ChatTest V1.1!\n") 
    def do_login(self,session,line):
        parts=line.strip().split(' ')
        name=parts[0]
        if not name:
            session.push("Please enter a name\n")
        elif name in self.server.users:
            session.push("The name %s is taken\n"%name)
        else:
            session.name=name
            try:
                roomName=parts[1] # 第二个参数作为聊天室
            except IndexError:
                roomName="main" # 如果没有第二个参数，就默认加入主聊天室（默认的）
            if not roomName in self.server.rooms:
                self.server.createRoom(roomName)
            session.enter(self.server.rooms[roomName])


    def unknow(self,session,line):
        session.push("commands:login logout list\n")

class ChatRoom(Room):
    def add(self,session):
        session.push("Welcome to ChatRoom: %s!\n"%self.roomName)
        self.broadcast(session.name+" has entered the room\n")
        Room.add(self,session)
        self.server.users[session.name]=session

    def remove(self,session):
        Room.remove(self,session)
        self.broadcast(session.name + " has left the room\n")

    def do_say(self,session,line):
        self.broadcast("%s: %s\n"%(session.name,line))

    def do_look(self,session,line):
        session.push("list for room:\n")
        for i,other in zip(range(len(self.sessions)),
                self.sessions):
            session.push(str(i)+': '+other.name+'\n')

    def do_to(self,session,line):
        try:
            parts=line.split(' ',1)
            name=parts[0]
            line=parts[1]
            toUser=self.server.users[name]
            toUser.push("%s: %s\n"%(session.name,line))
        except IndexError:
            session.push("Usage:/to toUser line\n")
            return False
        except KeyError:
            session.push("%s does not exist!\n"%name)
            return False
        
        

    def do_exit(self,session,line):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass
        session.enter(LoginRoom(self.server))

    def do_who(self,session,line):
        session.push("list for server:\n")
        for i,name in zip(range(len(self.server.users)),
                self.server.users.keys()):
            session.push(str(i) + ': '+name+'\n')

class LogoutRoom(Room):
    def add(self,session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass
        
class ChatSession(async_chat):
    def __init__(self,server,sock):
        async_chat.__init__(self,sock)
        self.server=server
        self.set_terminator("\n")
        self.data=[]
        self.name=None
        self.enter(LoginRoom(server,""))

    def enter(self,room):
        try:
            cur=self.room # 如果没有self.room（就是刚登录时）
        except AttributeError:
            pass
        else:
            cur.remove(self) # 退出时会执行
        self.room=room
        room.add(self)

    def collect_incoming_data(self,data):
        self.data.append(data)
        print data


    def found_terminator(self):
        line=''.join(self.data)
        self.data=[]
        try:
            self.room.handle(self,line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class ChatServer(dispatcher):
    def __init__(self,port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("",port))
        self.listen(5)
        self.users={}
        self.main_room=ChatRoom(self,"main")
        self.rooms={"main":self.main_room}

    def createRoom(self,name):
        self.rooms[name]=ChatRoom(self,name)

    def handle_accept(self):
        conn,addr=self.accept()
        print 'connected from ',addr
        ChatSession(self,conn)

if __name__=="__main__":
    s=ChatServer(1440)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
