#coding:utf8
from config import render,get_isLoginOk,db
import web
class login:
    def GET(self):
        try:
            userName=web.cookies().user
            passWord=web.cookies().pwd
            uid=get_isLoginOk(userName,passWord)
            if uid==0:
                raise web.seeother('/linux')
            else:
                raise web.seeother('/list')
        except Exception,e:
            print e
            return render.loginuser()
class logout:
    def GET(self):
        web.setcookie("user","",1)
        web.setcookie("pwd","",1)
        raise web.seeother('/')

class loginPost():
    def POST(self):
        import hashlib
        data=web.input()
        userName=data.User
        userPwd=hashlib.md5(data.Pwd).hexdigest()
        try:
            uid=get_isLoginOk(userName,userPwd)
            web.setcookie("user",userName)
            web.setcookie("pwd",userPwd)
            self.setLastTime(userName)   
            if uid!=0: # 成员用户显示故障表 
                raise web.seeother('/list')
            else:
                raise web.seeother('/linux') #管理员用户，显示管理后台
        except:
            return render.loginuser("用户名或密码出错!")

    def setLastTime(self,user):
        import time
        db.update('accounts',where="UserName=\'%s\'"%user,
                LastTime="%s"%time.strftime("%Y-%m-%d %H:%M:%S",
                    time.localtime()))


