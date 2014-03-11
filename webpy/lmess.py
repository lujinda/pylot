#coding:utf8
from config import *
def getData():
	return db.select('lmess',order='Id DESC')
class messBoard:
	def GET(self,e=None):
		return render.messB(getData(),e)
class lmess(messBoard):
	def POST(self):
		data=web.input()
		if isEmpty(data.Name) or isEmpty(data.Content):
			return render.messB(getData(),"请检查您的留言信息是否有填写错误!")
		db.insert("lmess",Name=data.Name,Content=data.Content,Time=time.strftime("%Y-%m-%d %T",time.localtime()))
		raise web.seeother('/messBoard')
	def GET(self):
		raise web.seeother('/messBoard')
