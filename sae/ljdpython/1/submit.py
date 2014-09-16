#coding:utf8
import re
import web
from config import render,db,send_mail,succMess

__all__ = ["sendSubmit"]

def check_phone(phone):
    if re.match(r"^\d{6}$|^\d{11}$",phone):
        return True
    else:
        return False

def check_name(name):
    return 2<= len(name) <= 15

def check_content(content):
    return len(content) >= 10

        

class sendSubmit:
    def POST(self):
        data=web.input()  # post的数据
        if not check_phone(data.Phone):
            return render.frame.main("请填写正确的号码（短号或长号）")   

        if not check_name(data.Name):
            return render.frame.main("亲，您的名字有这么长吗？")
            
        if not check_content(data.Content):
            return render.frame.main("亲，故障请写得稍微详细点哦～")
        
        try:
            self.writeDb(data)
           # __subject=u"在%s 有人向求助我们!"%self.postTime
           # __message=u"故障:%s\n用户姓名:%s 寝室:%s 联系方式:%s\n正式的小伙伴们，快去帮帮他吧~"%(data.Content,
            #        data.Name,data.Room,data.Phone)
            #send_mail().sendMail(__subject,__message)
            
            return render.success(succMess)
        except Exception,e:
            return render.frame.main("提交失败")
    
    @classmethod
    def writeDb(self,data):
        import time
        self.postTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        
        db.insert("bugs",Content=data.Content,Name=data.Name,
                Phone=data.Phone,Room=data.Room,
                PostTime=self.postTime,
                IsOver=0,
                Time=data.Time,
                )
        
