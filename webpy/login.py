#coding:utf8
from config import *
import hashlib
class login:
	def GET(self):
		return render.loginUser()
class loginPost(login):
	def POST(self):
		data=web.input()
		userName=data.User
		userPwd=hashlib.md5(data.Pwd).hexdigest()
		if isEmpty(userName) or isEmpty(userPwd):
			return render.loginUser("请不要输入空白的用户名和密码哦")
		if authUser(userName,userPwd)==0:
			return render.loginUser('密码或用户不匹配')
		self.loginOk(userName,userPwd)
		return render.inORout("successful login")
	def loginOk(self,user,pwd):
		web.setcookie("user",user)
		web.setcookie("pwd",pwd)
class logout():
	def GET(self):
		web.setcookie("user","",1)
		return render.inORout("successful logout")
