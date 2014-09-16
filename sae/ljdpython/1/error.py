#coding:utf8
from config import render
import web

def notfound():
    return web.notfound(render.notfound())

def internalerror():
    return web.internalerror("""<html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <h3>对服务器的请求，暂时出现了点问题，请刷新，或过会儿再尝试！</h3>
        如果发现经常出错，请联系作者670913
    </html>""")
