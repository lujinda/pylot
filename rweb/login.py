from config import *
import hashlib
class Login:
    def GET(self):
        return render.loginUser()
class Logout:
    def GET(self):
        web.setcookie('user','')
        web.setcookie('pwd','')
        raise web.seeother('/login')
class CheckLogin:
    def POST(self):
        data=web.input()
        username=data.User
        password=hashlib.md5(data.Pwd).hexdigest()
        self.loginOk(username,password)
        return web.seeother('/frame/main.html')
    def loginOk(self,user,pwd):
        web.setcookie('user',user)
        web.setcookie('pwd',pwd)
        

