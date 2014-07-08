#coding:utf8
from config import *
from submit import *
from listbug import *
from login import *
from admin import *

class index:
    def GET(self):
        return render.index()
class readTop:
    def GET(self):
        buglist=get_bugsList()
        return render.frame.top(buglist.yes,buglist.no)

class readMain:
    def GET(self):
        return render.frame.main()

class readRight:
    def GET(self):
        return render.frame.right(get_mess(),get_listDb())


app=web.application(urls,globals()).wsgifunc()
application=sae.create_wsgi_app(app)
