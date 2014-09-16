#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-31 11:20:44
# Filename        : twisted/plugins/echo.py
# Description     : 
from twisted.application import internet,service
from twisted.plugin import IPlugin
from twisted.cred import credentials,portal,strcred
import sys
import os
sys.path.append(os.getcwd())
from tw_cred import EchoFactory,Realm

from twisted.python import usage
from zope.interface import implements

class Options(usage.Options,strcred.AuthOptionMixin):
    supportedInterfaces=(credentials.IUsernamePassword,)
    optParameters=[
            ["port",'p',1234,"The port number to listen on."]
            ]

class EchoServiceMaker(object):
    implements(service.IServiceMaker,IPlugin)
    tapname="echo"
    description="A TCP-base echo server."
    options=Options

    def makeService(self,options):
        p=portal.Portal(Realm(),options["credCheckers"])
        return internet.TCPServer(int(options['port']),EchoFactory(p))
serviceMaker=EchoServiceMaker()

