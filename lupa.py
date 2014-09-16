import cookielib
import urllib2
import urllib
import threading



class Lupa(object):
    def __init__(self):
        cj=cookielib.LWPCookieJar()
        cjProcess=urllib2.HTTPCookieProcessor(cj)
        opener=urllib2.build_opener(cjProcess)
        urllib2.install_opener(opener)

    def login(self,username,password):
        post_data={"username":username,"password":password,"autologin":"0","iscompanay":"1"}
        post_data=urllib.urlencode(post_data)
        login_url="http://w5.lo.lupa.cn/index.php?app=account&ac=login&ts=do"
        for i in range(2):
            req=urllib2.Request(login_url,post_data)
            page=urllib2.urlopen(req)
            print page.read()

    def check(self):
        url="http://w5.lo.lupa.cn/index.php?app=company&ac=job&ts=activejob"
        print urllib2.urlopen(url).read()
    
    def req(self,username,password):
        req_url="http://w5.lo.lupa.cn/index.php?app=company&ac=reg&ts=mail"
        post_data={"email":username,"password":password,"protocol":"checked",
                "com_name":password,"com_phone":'1'}
        post_data=urllib.urlencode(post_data)
        req=urllib2.Request(req_url,post_data)
        print urllib2.urlopen(req).read()

    def create(self):
        import random
        create_url="http://w5.lo.lupa.cn/index.php?app=company&ac=job&ts=create"
      #  jobtype=6&name=python&minsalary=0&maxsalary=0&workplacepid=1&workplacecid=2&degree=0&worktype=1&description=python&paperid=0&schoolid=
        post_data={"jobtype":6,"name":"python","minsalary":'1000',"maxsalary":'%s'%(random.randint(3000,4000)),
                "workplacepid":'1','degree':'0','worktype':'1',
                "workplacecid":'2',
                'description':'python'}
        post_data=urllib.urlencode(post_data)
        req=urllib2.Request(create_url,post_data)
        try:
            urllib2.urlopen(req)

        except:
            pass


if __name__=="__main__":
    lupa=Lupa()
#    lupa.req("q888888@qq.com","zxc123")
    tlist=[]
    lupa.req("q30@qq.com","zxc123")
    for i in range(2):
        t=threading.Thread(target=lupa.create)
        t.start()
        tlist.append(t)

    for t in tlist:
        t.join()
        
    lupa.check()
        

