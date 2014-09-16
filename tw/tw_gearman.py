#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-28 16:46:33
# Filename        : tw_gearman.py
# Description     : 

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource,ErrorPage
from template import render
from gearman import GearmanClient

temp=render('temp/')
new_client=GearmanClient(["192.168.8.116:1234"])

class PinYin(Resource):
    def getChild(self,name,request):
        return self
    def render_GET(self,request):
        return temp.pinyin()

    def render_POST(self,request):
        line=request.args["words"][0]
        return new_client.submit_job('pinyin',line).result

site=Site(PinYin())
reactor.listenTCP(1235,site,interface='0.0.0.0')
reactor.run()

