#coding:utf8
from config import get_isLoginOk,db,render,PageSize
import web

class sendKw():
    def getIsLogin(self):
        try:
            username=web.cookies().user
            password=web.cookies().pwd
            self.uid=get_isLoginOk(username,password)
            return True
        except:
            return False

    def GET(self):
        pageSize=PageSize/2
        data=web.input()

        try:
            bug=db.select("bugs",
                    where="IsOver = 1 and Pid = %s"%int(data.pid))[0]
            isLogin=self.getIsLogin()
            return render.result(bug,isLogin)
        except Exception,e:
            print e
            pass

        words=data.Kw.strip() # 取出 关键字成分

        if len(words)<2 or len(words) >30 :
            return render.frame.main("搜索引擎不喜欢太短或太长哦!!\n2-30字最好！")
        reStr=self.__getRe(words)
        page=self.getPage(data)
        bugslist=db.select("bugs",where="IsOver = 1 and Content REGEXP '%s'"%reStr,
                limit=pageSize,offset=pageSize*(page-1))

        return render.seeresult(bugslist,words,page)
    
    def getPage(self,data):
        try:
            page=int(data.page)
        except:
            page=1
        return page
        
    def __getRe(self,words):
        import re
        ignoreStr="了不哦啦啊吧吗呢的嘛".decode("utf8")
        res=[]
        def swChar(char):
            if char in r'\.*|-':
                return r'\\'+char
            else:
                return char
        for word in words.split():
            s=map(swChar,word)
            res.append('.{0,5}'.join(s))
        reStr='|'.join(res)
        reStr=re.sub(r"(?P<name>%s)"%'|'.join(ignoreStr),
                lambda x:'.',reStr)
        
        return reStr

