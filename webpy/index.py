#coding:utf8
from signup import *
from lmess import *
from login import *
def getUser():
	try:
		user=web.cookies().user
	except:
		user=""
	finally:
		return user
class index:
	def GET(self):
		try:
			db.transaction() #test the connection
		except Exception:
			return render.error(ERROR_DB)
		return render.index()
class readTop:
	def GET(self):
		return render.frame.top(getUser())
class readMain:
	def GET(self):
		return render.frame.main(getUser())
class readRight:
	def GET(self):
		return render.frame.right()
class error404:
	def GET(self):
		return render.error(ERROR_404)#4040 file not found
if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()
