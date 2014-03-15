#coding:utf8
from config import *
import hashlib
class Change:
    def GET(self):
        if not isLogin():raise web.seeother('/login')
        return render.changeUser()
class ChangePost:
    def POST(self):
        if not isLogin():raise web.seeother('/login')
        data=web.input()
        if data.Pwd!=data.aPwd:
            return render.changeUser('请确认两次输入的密码相同。')
        username=data.User
        password=hashlib.md5(data.Pwd).hexdigest()
        changeKey(username,password)
        self.loginOk(username,password)
       # (username,password)
        
        
    def loginOk(self,user,pwd):
        web.setcookie('user',user)
        web.setcookie('pwd',pwd)
        

