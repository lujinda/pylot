#coding:utf8
import web
from config import render,db,get_bugsList,CheckLogin,PageSize
Order="asc"
Page=1

class ListBug(CheckLogin):
    MESS= """
    <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    该故障已不存在，下次要点得快哦亲～谢谢你的参与!<br>
    <a href="/nolist">未解决列表</a>  <a href="/yeslist">已解决列表</a>
    </html>
            """
    def setOrder(self,data):
        global Order
        global Page
        try:
            if data.order=="desc":
                Order="desc"
            else:
                Order="asc"
            Page=1
        except:
            pass
        return Order

    def handler(self,cmd,line):
        try:
            meth=getattr(self,"do_"+cmd.strip(),None)
            meth(line.strip())
        except TypeError:
            pass
    
    def getPage(self,data):
        try:
            global Page
            Page=int(data.page)
        except:
            pass
        return Page
    
class noList(ListBug):
    def GET(self):
        data=web.input()   
        order=self.setOrder(data)
        page=self.getPage(data)
        for cmd,line in data.items():
            self.handler(cmd,line)
        bugslist=db.select('bugs',where="IsOver <> 1",order="Pid %s"%order,
                limit=PageSize,offset=(page-1)*PageSize)
        
        return render.nolist(bugslist,order,page)
    
    def do_del(self,line):
        db.delete("bugs",where="Pid =%d and IsOver = 0"%int(line))

class yesDeal(ListBug):
    def GET(self):
        data=web.input()
        if data.has_key("add"):
            pid=data["add"]
            bug=db.select("bugs",where="Pid =%s and IsOver=0"%pid)
            if not bug:
                return self.MESS
            else:
                return render.yesdeal(pid,bug[0])
        
class yesList(ListBug):
    def GET(self):
        data=web.input()
        order=self.setOrder(data)
        page=self.getPage(data)
        if data.has_key("del"):self.do_del(data["del"])

        bugslist=db.select('bugs',where="IsOver = 1",order="YesTime %s"%order,
                limit=PageSize,offset=(page-1)*PageSize)
        return render.yeslist(bugslist,order,self.uid,page)
    
    def do_del(self,pid):
        if self.uid==0:
            db.delete("bugs",where="Pid = %d and IsOver = 1"%int(pid))
    

class yesDealPost(ListBug):
    def POST(self):
        import time
        data=web.input()
        try:
            bug=db.update("bugs",where="Pid = %s and IsOver=0"%data.YesPid,
                YesWhy=data.YesContent,
                IsOver=1,YesNo=data.YesNo,
                YesTime=time.strftime("%Y-%m-%d %T",time.localtime()))
        except:
            return "提交失败，请返回重试"
        if not bug:
            return self.MESS
        else:
            raise web.seeother('/list')
            
