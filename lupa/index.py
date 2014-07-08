#coding:utf8
from config import *
class index(Resolve):
    def GET(self):
        data=web.input()
        if not self.getKeyPost():
            d=db.select(db_table,where="first = 0 and (invisible = -2 or invisible = 0)")
            self.resolveData(d)
        for cmd,line in data.items():
            self.handler(cmd,line)
        return render.index(self.getKeyPost())

    def do_no(self,line):
        try:
            del self.data_key[int(line)]
        except KeyError:
            pass

    def do_del(self,line):
        self.do_no(line)
        db.delete(db_table,where="pid = %s"%str(line))

    def do_clear(self,line):
        if line=="yes":
            self.data_key.clear()
            raise web.seeother('/')

    def do_delall(self,line):
        if line=="yes":
            try:
                self.delall()
                self.data_key.clear()
                raise web.seeother('/')
            except Exception,e:
                print e
            
    def delall(self):
        from itertools import imap
        
        if len(self.data_key.keys())==0:
            return None
        
        line="pid = %s and invisible = -2"%(' or pid = '.join(imap(str,self.data_key.keys())),
                )
        d=db.delete(db_table,where=line)
        
        
class result:
    def GET(self,mess):
        render.result(mess)
    
if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()
