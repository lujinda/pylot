#coding:utf8
import re,web,time
render=web.template.render("temp")
urls=(
		'/','index',
		)
web.config.debug=False
db_host='127.0.0.1'
db_dbn='mysql'
db_user='root'
db_pw='zxc123'
db_db='ultrax'
db=web.database(db_host,dbn=db_dbn,user=db_user,pw=db_pw,db=db_db)	#set database
code="utf8"

    
class Resolve():
    def __init__(self,data):
        self.lines=[]
        self.lines_key=[]
        for i  in data:
            self.lines.append(i.message)
            #print self.lines
        self.resolveData()

    def resolveData(self):
     #   self.isLike()
        self.isKey()

    def isKey(self):
        total=len(self.lines)
        re_http=re.compile(".*(h|H|ｈ|Ｈ).*?(t|T|Ｔ|ｔ).*?(t|T|Ｔ|ｔ).*?(p|P|ｐ|Ｐ).*".decode(code),re.U)
        # 匹配各种http开头
        re_qq=re.compile("(q|Q|ｑ|Ｑ|抠)((q|Q|ｑ|Ｑ|抠)?.{0,5}\d)".decode("utf8"))
        # 匹配大多数qq情况
        re_url=re.compile("\w+?\.(com|org|net)".decode("utf8"))
        for line in self.lines:
            if re_http.search(line) or re_qq.search(line) \
                    or re_url.search(line):
                self.lines_key.append(line)

    def getKeyLine(self):
        return self.lines_key
        
    def isLike(self):
        like_string=self.getLike()
        total=0
        for word in like_string:
            for line in self.lines:
                total+=line.count(word)
        g=float(total)/len((''.join(self.lines)))
        print "相似程度%f"%g
        if g>0.6:return True
        else:return False

    def getLike(self):
        set_result=set(self.lines[0])
        for i in self.lines[1:]:
            set_result=set_result & set(i)
        return ''.join(set_result)
        
