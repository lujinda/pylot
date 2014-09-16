#coding:utf8
import web
class query:
    def POST(self):
        data=web.input()
        postData={
                'userName':str(data.userName),
                'passwd':str(data.passwd),
                }

        student,count=self.login(postData)
        No,name=student
        mess=u"学号:%s 姓名:%s 晨跑数:%s"%(No,
                name,count)
        
        
        return mess

    def login(self,postData):
        import urllib
        import urllib2
        import cookielib
        url="http://share.zjtie.edu.cn/student/checkUser.jsp?"+urllib.urlencode(postData)
        seeUrl="http://share.zjtie.edu.cn/student/queryExerInfo.jsp"
        cj=cookielib.LWPCookieJar()
        cjProcess=urllib2.HTTPCookieProcessor(cj)
        opener=urllib2.build_opener(cjProcess,urllib2.HTTPHandler())
        urllib2.install_opener(opener)

        urllib2.urlopen(url,timeout=3)
        result=urllib2.urlopen(seeUrl,timeout=3).read().decode("gbk")
        import re
        re_info=re.compile(r"学号:(\d{8}).*?姓名:(.+?)<".decode("utf8"))
        re_count=re.compile(r"(\d+).*次".decode("utf8"),re.M)

        name=re_info.findall(result)[0]
        count=re_count.findall(result)[0]
        return name,count
