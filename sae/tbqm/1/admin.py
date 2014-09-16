#coding:utf8
from config import render,db,CheckLogin,get_listDb,get_mess
import web

class Admin(CheckLogin):
    def __init__(self):
        CheckLogin.__init__(self)
        if self.uid!=0:
            raise web.seeother('/login')

    def GET(self):
        return "亲，您打开的方式不对哦"

class adminIndex(Admin):
    def GET(self):
        return render.admin.index()

class areadTop:
    def GET(self):
        return render.admin.frame.top()
class areadMain:
    def GET(self):
        return render.admin.frame.main()

class setList(Admin):
    def GET(self):
        return render.admin.setlist(get_listDb())
class setListPost(setList):
    def POST(self):
        data=web.input()
        self.setDb(data.Content)
        return "技术人员名单更新完成"

    def setDb(self,data):
        import re
        db.delete("listdb",where="Name LIKE \"%\"")
        for line in data.splitlines():
            if re.match(r"^\d{8}-.{1,10}-(\d{6}|\d{11})$",line.strip()):
                no,name,phone=line.split('-')
                db.insert("listdb",No=no,Name=name,Phone=phone,Total=0)

class clearBugsList(Admin):
    def GET(self):
        return render.admin.clearbugslist()
class clearBugsListPost(Admin):
    def POST(self):
        db.delete("bugs",where="Name LIKE \"%\"")
        return "故障已被清空"

class setMess(Admin):
    def GET(self):
        return render.admin.setmess(get_mess())

class setMessPost(Admin):
    def POST(self):
        mess=web.input().Content
        db.update("info",where="Name=\"mess\"",Content=mess)
        return "公告更新完成"
        
class setKey(Admin):
    def GET(self):
        return render.admin.setkey()

class setKeyPost(Admin):
    def changeKey(self,data,uid):
        import re
        import hashlib
        user=data.Name.strip()
        pwd1=data.Pwd1.strip()
        pwd2=data.Pwd2.strip()
        u_r=re.compile(r"^\w{1,10}$")
        p_r=re.compile(r"^[\x21-\x7e]{5,16}$")
        if pwd1!=pwd2:raise Exception
        if u_r.match(user) and p_r.match(pwd1):
            db.update("accounts",where="Uid=%d"%int(uid),
                    UserName=user,
                    PassWord=hashlib.md5(pwd1).hexdigest())
        else:
            raise Exception
            
class rsetKeyPost(setKeyPost):
    def POST(self):
        data=web.input()
        import hashlib
        try:
            self.changeKey(data,0)
            web.setcookie("user",data.Name.strip())
            web.setcookie("pwd",hashlib.md5(data.Pwd1.strip()).hexdigest())
            return "管理员账号密码修改成功，请牢记。下次用新账号密码登录"
        except:
            return render.admin.setkey("操作失败<br>请检查密码长度，或两次密码输入是否统一")

class osetKeyPost(setKeyPost):
    def POST(self):
        data=web.input()
        try:
            self.changeKey(data,1)
            return "协会成员账号修改成功，快把新账号密码告诉小伙伴们吧~"
        except:
            return render.admin.setkey("操作失败<br>请检查密码长度，或两次密码输入是否统一")


class seeResult(Admin):

    def getNo(self):
        data=db.select("listdb",where="No REGEXP '[0-9]{8}'")
        No_list={i.No:i for i  in data}
        return No_list
       
    def GET(self):
        No_list=self.getNo()
        data=db.select("bugs",
                where="YesNo REGEXP '^(%s)$'"%('|'.join(No_list.keys())),
                what="YesNo,count(*) as Count",group="YesNo")

        for i in data:
            try:
                No_list[i.YesNo].Total=i.Count
            except KeyError:
                pass

        return render.admin.seeresult(No_list.values())
