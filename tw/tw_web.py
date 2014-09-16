#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-26 13:01:06
# Filename        : tw_web.py
# Description     : 

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource,ErrorPage
import sys
import tw_config as config

# 传入一个request,返回是否已登录
class AuthUser():
    def __init__(self,request):
        self.request=request
        self.__read_pwd()
        self.auth_user()

    def __read_pwd(self):
        try:
            pwd_fd=open(config.PWD_PATH,'r')
            self.user_pwd=map(lambda x:tuple(x.strip().split(':')),
                pwd_fd.readlines())
            pwd_fd.close()
        except OSError:
            print "pwdfile not exist!"
            sys.exit(1)


    def auth_user(self):
        user=self.request.getUser()
        password=self.request.getPassword()
        if (user,password) in self.user_pwd:
            return True

        else:
            return False

class BrowseFile(Resource):
    def getChild(self,name,request):
        if AuthUser(request).auth_user():
            resource=self.get_resource(request.getUser())
            return resource
            
        else:
            request.setHeader('WWW-Authenticate',
                    "Basic realm=\"your ip: %s\""%
                    (request.getClientIP()))

            return ErrorPage(401,"Need authenticated","%s"%
                    (request.getAllHeaders()))


    def get_resource(self,username):
        __path=config.USERPATH.get(username,None)
        if __path:
            return File(__path)
        else:
            return File(config.PATH)
        
resource=BrowseFile()
factory=Site(resource)
factory.logPath="/tmp/browsefile.log"
reactor.listenTCP(config.PORT,factory)
reactor.run()

