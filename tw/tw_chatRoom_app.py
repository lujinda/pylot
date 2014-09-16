from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory
from twisted.internet import defer
from twisted.protocols.basic import LineReceiver
from twisted.python import log


LOGPATH="/tmp/chatRoom.log"

class commaneHandler:
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
        session.write("%s:unknow command!\n"%cmd)

                
class Room(commaneHandler):
    def __init__(self,server,name=""):
        self.server=server
        self.roomName=name
        self.sessions=[]

    def add(self,session):
        self.sessions.append(session)

    def remove(self,session):
        try:
            self.sessions.remove(session)
        except KeyError:
            pass

    def broadcast(self,line):
        for session in self.sessions:
            session.write(line+'\n')
    
    def do_list(self,session,line):
        session.write("list for ChatRoom\n")
        for room in self.server.rooms:
            session.write(room+'\n')
    
    def do_logout(self,session,line):
        session.entry(LogoutRoom(self.server))
        session.d.errback(None)

class LoginRoom(Room):
    def add(self,session):
        Room.add(self,session)
        log.msg("Connection from %s "%session.session.getPeer())
        session.write("Welcome to ChatTest for twisted v1.1!\n")
    def do_login(self,session,line):
        parts=line.strip().split(" ")
        name=parts[0]
        if not name:
            session.write("Please entry a name\n")
        elif name in self.server.users:
            session.write("The name %s is token\n"%name)
        else:
            session.name=name
            try:
                roomName=parts[1]
            except IndexError:
                roomName="main"
            
            if not roomName in self.server.rooms:
                self.server.createRoom(roomName)
            session.entry(self.server.rooms[roomName])
    
    def unknow(self,session,line):
        session.write("Commands:login logout list\n")

class LogoutRoom(Room):
    def add(self,session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass

class ChatRoom(Room):
    def add(self,session):
        session.write("Welcome to ChatRoom:%s !\n"%self.roomName)
        mess=session.name+" has join the room"
        self.broadcast(mess)
        log.msg(mess)
        Room.add(self,session)
        self.server.users[session.name]=session
    
    def remove(self,session):
        Room.remove(self,session)
        self.broadcast(session.name+" has left the room")
        
    def do_say(self,session,line):
        self.broadcast("%s: %s"%(session.name,line))

    def do_look(self,session,line):
        session.write("list for room:\n")
        for i,other in enumerate(self.sessions):
            session.write("%d: %s\n"%(i,other.name))

    def do_exit(self,session,line):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass
        session.entry(LoginRoom(self.server))

    def do_to(self,session,line):
        try:
            parts=line.split(' ',1)
            name=parts[0]
            line=parts[1]
            toUser=self.server.users[name]
            toUser.write("%s: %s\n"%(session.name,line))
        except IndexError:
            session.write("Usage:/to toUser line\n")
            return False
        except KeyError:
            session.write("%s does not exist!\n"%name)
            return False
        
    def do_who(self,session,line):
        session.write("list for server:\n")
        for i,name in enumerate(self.server.users.keys()):
            session.write("%d: %s\n"%(i,name))

class chatSession:
    def __init__(self,server,session,d):
        self.d=d
        self.server=server
        self.session=session
        self.name=None
        self.entry(LoginRoom(self.server,""))

    def write(self,line):
        self.session.write(line)

    def entry(self,room):
        try:
            cur=self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room=room
        room.add(self)

    def execComm(self,line):
        self.room.handle(self,line.strip())

class ChatProtocol(LineReceiver):
    
    def connectionMade(self):
        d=defer.Deferred()
        d.addBoth(self.endSession)
        self.s=chatSession(self.factory,self.transport,d)
    
    def endSession(self,_):
        self.transport.loseConnection()

    def connectionLost(self,reason):
        pass
    
    def connectionFailure(self,connector,reason):
        print reason


    def lineReceived(self,line):
        self.s.execComm(line)

class ChatFactory(Factory):
    protocol=ChatProtocol
    def __init__(self):
        self.users={}
        self.rooms={}
        self.createRoom("main")

    def createRoom(self,name):
        self.rooms[name]=ChatRoom(self,name)
        

