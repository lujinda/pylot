#coding:utf8
from config import *
class SetNet:
    def GET(self):
        if not isLogin():raise web.seeother('/login')
        return render.setnetwork()
class SetDns:
    def POST(self):
        data=web.input()
        self.setDns(data.Dns1,data.Dns2)
        web.seeother('/setnet')
    def setDns(self,dns1,dns2):
        fd=open('/etc/resolv.conf','w')
        if dns1:fd.write('nameserver %s\n'%dns1)
        if dns2:fd.write('nameserver %s\n'%dns2)
        fd.close()
