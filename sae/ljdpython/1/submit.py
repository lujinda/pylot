#coding:utf8
import re
import web
from config import render,db,send_mail

class sendSubmit:
    def POST(self):
        data=web.input()  # post的数据
        if not self.check(data.Phone,r"^\d{6}$|^\d{11}$"):
            return render.frame.main("请填写正确的号码（短号或长号）")   

        if len(data.Name)>15:
            return render.frame.main("亲，您的名字有这么长吗？")
            
        if len(data.Content)<10:
            return render.frame.main("亲，故障请写得稍微详细点哦～")
        
        try:
            self.writeDb(data)
            __subject=u"在%s 有人向求助我们!"%self.postTime
            __message=u"故障:%s\n用户姓名:%s 寝室:%s 联系方式:%s\n正式的小伙伴们，快去帮帮他吧~"%(data.Content,
                    data.Name,data.Room,data.Phone)
            #send_mail().sendMail(__subject,__message)
            
            return render.frame.main("您的故障情况，我会已收到<br>我们会尽快联系您")
        except Exception,e:
            return render.frame.main("提交失败")

    def writeDb(self,data):
        import time
        self.postTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        
        db.insert("bugs",Content=data.Content,Name=data.Name,
                Phone=data.Phone,Room=data.Room,
                PostTime=self.postTime,
                IsOver=0,
                Time=data.Time,
                )
        
    def check(self,data,r):
        if re.match(r,data):
            return True
        else:
            return False
        

