import web,urllib
from googleTran import *
render=web.template.render('temp') #read template
web.config.debug=False		#close Debug
urls=('/','index','/tran','tran')	#/ to index class,/tran to tran class
class index:
	def GET(self):
		return render.tran()	#show index
class tran:
	def POST(self):
		i=web.input()	#read data
		try:
			data=get_tran(urllib.urlencode(get_zORe(i.content.encode('utf8'))))	
		except Exception,e:
			raise web.seeother('/')#if the translation fails,the return index
		return render.tran(i.content,data)
if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()
