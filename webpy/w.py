#coning:utf8
import web
import time
render=web.template.render('temp') #read template
web.config.debug=False	#close debug
urls=('/','index','/add','add')	#when access to the root ,use the index class
db=web.database('127.0.0.1',dbn='mysql',user='root',pw='zxc123',db='l_mess')
#connect to the database
class index:
	def GET(self):
		mess=db.select('l_mess')#show
		return render.index(mess)
class add:
	def POST(self):
		i=web.input()
		n=db.insert('l_mess',Name=i.name,Content=i.content,Time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
		raise web.seeother('/')#redirected to '/'
if __name__ == '__main__':
	app=web.application(urls,globals())#create an app,global search class
	app.run() 

