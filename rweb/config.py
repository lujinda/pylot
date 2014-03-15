import web,time
import os
import shelve
import hashlib
import re
render=web.template.render('temp')
urls=(
        '/','index',
        '/login','Login',
        '/setnet','SetNet',
        '/setnet/setDnsPost','SetDns',
        '/login/loginPost','CheckLogin',
        '/change','Change',
        '/change/changePost','ChangePost',
        '/logout','Logout',
        '/frame/top.html','readTop',
        '/frame/main.html','readMain',
        '/frame/right.html','readRight',
        )
userDbUrl='./userKey.db'
def openDb(dbUrl):
    return shelve.open(dbUrl,'c')
def isLogin():
    db=openDb(userDbUrl)
    try:
        username=db['username']
        password=db['password']
    except:
        username='root'
        password=hashlib.md5('root').hexdigest()
    finally:
        db.close()
    try:
        if username==web.cookies().user and password==web.cookies().pwd:
            return True
        else:
            return False
    except:
        return False

def changeKey(user,pwd):
    db=openDb(userDbUrl)
    db['username']=user
    db['password']=pwd
    db.close()

class getSysInfo:
    def getDns(self):
        dnsFile=open('/etc/resolv.conf','r')
        return re.findall(r'\s(.+)\s?',dnsFile.read())
    def execP(self,comm):
        p=os.popen(comm)
        data=p.read()
        p.close()
        return data.split('\n')
