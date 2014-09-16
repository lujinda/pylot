#coding:utf8
from config import *

class img:
    def GET(self):
        return "Hi"

app=web.application(urls,globals())
app=app.wsgifunc()
application=sae.create_wsgi_app(app)

