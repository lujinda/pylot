#coding:utf8
from config import *
import hashlib
class signup:
	def GET(self):
		return render.reg()#show registration page

class getAccount(signup):
	def POST(self):
		data=web.input()
		if not self.check(data.User,u_r):
			return render.reg('创建用户失败，用户名由6-20字母数字组成') #passing messages
		if not self.check(data.Pwd,u_r):
			return render.reg('密码由6-20字符组成，不允许包括空格和中文及特殊符号')
		if not self.check(data.Email,e_r):
			return render.reg('请输入合法的E-mail地址')
		if self.checkIn(data.User,data.Email):
			return render.reg('您注册的用户或邮箱已被人抢注，请更改')

		self.cAccount(data)
		return render.welcome(data)
	def checkIn(self,user,email):
		return len(db.select('accounts',where="username=\'%s\' or email=\'%s\'"%(user,email)))
	def check(self,s,r):
		if r.search(s):
			return True
		return False
	def cAccount(self,data):
		try:
			db.insert('accounts',username=data.User,password=hashlib.md5(data.Pwd).hexdigest(),email=data.Email)#add account
		except Exception,e:
			raise web.seeother('/')#if you create a user fails to return index
