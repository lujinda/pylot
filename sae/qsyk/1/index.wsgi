#coding:utf8
import web
import BeautifulSoup
from config import *


class index:
    def GET(self):
        return "ok"


app=web.application(urls,globals())
app=app.wsgifunc()
application=sae.create_wsgi_app(app)
