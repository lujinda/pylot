from twisted.web import http

class MyRequestHandler(http.Request):
    pages={
            '/':'<h1>home</h1>homePage',
            '/test':'<h1>Test</h1>Test Page',

            }
    def process(self):
        self.setHeader("Content-Type","text/html;charset=UTF-8")
        if self.pages.has_key(self.path):
            self.write(self.pages[self.path])
        else:
            self.redirect('http://www.qq.com')
            self.setResponseCode(http.NOT_FOUND)
            self.write("<h1>Not Found</h1>Sorry,no such page.")
        self.finish()

class MyHttp(http.HTTPChannel):
    requestFactory=MyRequestHandler

class MyHttpFactory(http.HTTPFactory):
    protocol=MyHttp

if __name__=="__main__":
    from twisted.internet import reactor
    reactor.listenTCP(8000,MyHttpFactory())
    reactor.run()

