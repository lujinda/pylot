class handler:
    def callback(self,prefix,name,*args):
        method=getattr(self,prefix+name,None)
        if callable(method):return method(*args)
    def p(self,name):
        self.callback("p_",name)
class handlerP(handler):
    def p_abc(self):
        print "abc"

hand=handlerP()
hand.p("abc")
        
        
