#coding:utf8
from config import *
class index:
    def GET(self):
        d=db.select("pre_forum_post")
        lj=Resolve(d)
        return render.index(lj.getKeyPost())
if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()
