#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-26 09:31:33
# Filename        : tw_ftp.py
# Description     : 
from twisted.protocols import ftp
from twisted.cred import portal,checkers
from zope.interface import implements
from twisted.python import filepath

class FTPRealm:
    implements(portal.IRealm)

    def __init__(self,anonymousRoot):
        self.anonymousRoot=filepath.FilePath(anonymousRoot)
        self.dir={'ljd':"/tmp",'root':'/'}

    def requestAvatar(self,avatarId,mind,*interfaces):
        for iface in interfaces:
            if iface is ftp.IFTPShell:
                if avatarId is checkers.ANONYMOUS:
                    avatar=ftp.FTPAnonymousShell(self.anonymousRoot)
                else:
                    user_dir=self.dir[avatarId]
                    avatar=ftp.FTPShell(filepath.FilePath(user_dir))

                return ftp.IFTPShell,avatar,getattr(avatar,'logout',lambda:None)
        raise NotImplementedError("Only IFTPShell interface is supported by this realm")

portal=portal.Portal(FTPRealm('/data'))
portal.registerChecker(checkers.AllowAnonymousAccess())
portal.registerChecker(checkers.FilePasswordDB("pwd.txt"))
f=ftp.FTPFactory(portal)
from twisted.internet import reactor
reactor.listenTCP(1234,f)
reactor.run()
