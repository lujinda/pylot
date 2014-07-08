#coding:utf8
import sae
import sae.const
import web
import os
urls=(
        '/',"index",
        '/frame/top.html','readTop',
        '/frame/main.html','readMain',
        '/frame/right.html','readRight',
        '/sendSubmit','sendSubmit', #提交
        '/oklist','okList', #列出故障
        '/list','noList', #列出故障
        '/nolist','noList', #列出故障
        '/yeslist','yesList',
        '/yesDeal','yesDeal',
        '/yesDeal/post','yesDealPost',
        '/login/?','login', # 登录
        '/login/loginPost','loginPost',
        '/logout','logout',
        '/linux/?','adminIndex',
        '/admin/frame/top.html',"areadTop",
        '/admin/frame/main.html',"areadMain",
        '/admin/setList','setList', # 成员
        '/admin/setList/post','setListPost', # 成员
        '/admin/setMess','setMess', # 成员
        '/admin/setMess/post','setMessPost', # 成员
        '/admin/setKey','setKey',
        '/admin/setKey/rpost','rsetKeyPost',
        '/admin/setKey/opost','osetKeyPost',
        '/admin/clearBugsList','clearBugsList',
        '/admin/clearBugsList/post','clearBugsListPost',
        )
web.config.debug = False
app_root=os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
db=web.database(port=int(sae.const.MYSQL_PORT), host=sae.const.MYSQL_HOST,dbn="mysql",
        user=sae.const.MYSQL_USER,pw=sae.const.MYSQL_PASS,
        db=sae.const.MYSQL_DB)

def get_bugsList(): 
    class BugsList:
        yes=0
        no=0
        yeslist=[]
        nolist=[]
    buglist=BugsList()
    buglist.yeslist=db.select('bugs',where="IsOver = 1")
    buglist.nolist=db.select('bugs',where="IsOver <> 1")
    buglist.yes=len(buglist.yeslist)
    buglist.no=len(buglist.nolist)
    return buglist

def get_isLoginOk(user,password):
    data=db.select('accounts',
            where="UserName=\'%s\' and PassWord=\'%s\'"%(user,password))[0]
    return int(data.Uid)

class CheckLogin:
    def __init__(self):
        try:
            username=web.cookies().user
            password=web.cookies().pwd
            self.uid=get_isLoginOk(username,password)
        except:
            raise web.seeother("/login")


def get_listDb():
    listDb=[]
    for i in db.select("listdb"):
        listDb.append((i.No,i.Name,i.Phone))
    return listDb
def get_mess():
    d=db.select("info",where="Name = \"mess\"")
    if not d:
        db.insert("info",Name="mess",Content="")
        return ""
    return d[0].Content

class send_mail():
    def __init__(self):
        self.__username="ljd31415926@126.com"
        self.__password="3.1415926"
        web.config.smtp_server="smtp.126.com"
        web.config.smtp_port=25
        web.config.smtp_username=self.__username
        web.config.smtp_password=self.__password
        web.config.smtp_starttls=True

    def sendMail(self,__subject,__message):
        web.sendmail(self.__username,"q8886888@qq.com",__subject.encode("utf-8"),__message.encode("utf-8"))

    
