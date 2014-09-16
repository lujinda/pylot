#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-31 10:37:58
# Filename        : tw_cred.py
# Description     : 
from zope.interface import implements,Interface,implementer
from twisted.cred import checkers,credentials,portal
from twisted.internet import protocol,reactor

from twisted.protocols import basic

class IProtocolAvatar(Interface):
    def logout():
        """
        clean up per-login resources ollocated to this avator.
        """
    



class Avatar(object):
    implements(IProtocolAvatar)

    def logout(self):
        self.transport.loseConnection()

class EchoAvatar(Avatar):
    pass

class DoAvatara(Avatar):

    def do_comm(self,cmd,*args):
        from twisted.internet import utils
        output=utils.getProcessOutput(cmd,args=args,
                errortoo=True)
        output.addCallback(self.writeResponse)

    def writeResponse(self,result):
        self.transport.write(result)


class Echo(basic.LineReceiver):
    protal=None
    avatar=None
    logout=None
    delimiter='\n'

    def cocnnectionLost(self,reason):
        if self.logout:
            self.logout()
            self.avater=None
            seslf.logout=None

    def lineReceived(self,line):
        if not self.avatar:
            username,password=line.strip().split(" ")+[]
            self.tryLogin(username,password)
        else:
            if line.lower().strip()=='quit':
                self.avatar.logout()
            try:
                line=line.strip()
                cmd_parser=line.split(' ',1)
                if len(cmd_parser)>1:
                    cmd=cmd_parser[0]
                    args=cmd_parser[1:]
                else:
                    cmd,args=cmd_parser[0],tuple()
                self.avatar.do_comm(cmd.strip(),*args)
            except AttributeError,e:
                self.sendLine(line)


    def tryLogin(self,username,password):
        self.portal.login(credentials.UsernamePassword(username,
            password),
            None,IProtocolAvatar).addCallbacks(self._cbLogin,
                    self._ebLogin)

    def _cbLogin(self,(interface,avatar,logout)):
        self.avatar=avatar
        self.logout=logout
        self.avatar.transport=self.transport
        self.sendLine("Login successful,please procees.")

    def _ebLogin(self,failure):
        self.sendLine("Login denied,goodbye.")
     #   print failure
        self.transport.loseConnection()

class EchoFactory(protocol.Factory):
    def __init__(self,portal):
        self.portal=portal

    def buildProtocol(self,addr):
        protocol=Echo()
        protocol.portal=self.portal
        return protocol
        
class Realm(object):
    implements(portal.IRealm)
    
    def requestAvatar(self,avatarId,mind,*interfaces):
        if avatarId=='root':
            avatar=DoAvatara()
        else:
            avatar=EchoAvatar()
        return None,avatar,avatar.logout

        raise NotImplementedError("This realm only supports the IProtocolAvatar interface.")

