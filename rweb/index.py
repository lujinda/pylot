#coding:utf8
from config import *
from login import *
from change import *
from setnet import *
class index:
    def GET(self):
        return render.index()
class readTop:
    def GET(self):
        return render.frame.top()
class readMain:
    def GET(self):
        if not isLogin():raise web.seeother('/login')
        return render.frame.main()
class readRight:
    def GET(self):
        sysInfo={}
        sysInfo['dns']=getSysInfo().getDns()
        return render.frame.right(sysInfo)
if __name__=='__main__':
    app=web.application(urls,globals())
    app.run()
