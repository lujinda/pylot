#coding:utf8
from twisted.internet import reactor,utils
from twisted.web import http
from template import render

temp=render('temp/')

class MyRequestHandler(http.Request):
    resource=['/']
    
    def certUser(self):
        user=self.getUser()
        password=self.getPassword()
        if not (user == 'ljd' and password=="zxc123"):
            self.setHeader('WWW-Authenticate',"Basic realm=\"Please input you key:\"")
            self.setResponseCode(401)
            return  None
            

    def process(self):
        self.certUser()
        self.setHeader('Content-Type','text/html')
        if self.path in self.resource:
            if self.method.upper()=="GET":
                self.write(temp.t())
            elif self.method.upper()=='POST':
                self.setHeader('Content-Type','text/plain')
                cmd,args=self.args['cmd'][0].split(' ',1)
                if args:
                    args=args.split()
                self.write("请稍等")
                d=utils.getProcessOutput(cmd,args,errortoo=True)
                d.addCallback(self.send_output)
                
                
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write("<h1>Not Found</h1>")
        

    def send_output(self,result):
        self.write(result)
        self.finish()

class MyHTTP(http.HTTPChannel):
    requestFactory=MyRequestHandler
    def connectionMade(self):
        print '%s'%(self.transport.getPeer())

class MyHTTPFactory(http.HTTPFactory):
    protocol=MyHTTP

reactor.listenTCP(1234,MyHTTPFactory())
reactor.run()

