#coding:utf8
import re
import wx
import shelve
import os
import mimetypes
import threading
import chardet
import sys
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.Encoders import encode_base64
from email.mime.base import MIMEBase

Db=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"mail.db")

def openDb(dbUrl):
    return shelve.open(dbUrl,'c')
def writeDb(db,key,value):
    db[key]=value
    db.close()
def readInfo(*args):
    db=openDb(Db)
    d={}
    for key in args:
        try:
            d[key]=db[key]
        except:
            break
    db.close()
    return d
def saveInfo(**kwargs):
    db=openDb(Db)
    for key in kwargs:
        db[key]=kwargs[key]
    db.close()
    

class WorkerThread(threading.Thread):
    def __init__(self,window,fun,*args):
        threading.Thread.__init__(self)
        self.window=window
        self.fun=fun
        self.args=args
    def run(self):
        wx.CallAfter(self.fun,*self.args)

class mailFrame(wx.Frame):
    def __init__(self,myEmail,smtp):
        wx.Frame.__init__(self,None,-1,myEmail,size=(500,400),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.smtp=smtp
        self.attrList=[]
        self.fromTo=myEmail
        self.panel=wx.Panel(self,-1)
        self.ShowElements()
        self.Center()
        self.Show()

    def ShowElements(self):
        x=10
        wx.StaticText(self.panel,-1,"收件人(多个请用';'分隔):",pos=(x,10))
        self.toText=wx.TextCtrl(self.panel,-1,"",pos=(x,30),size=(380,25))
        wx.StaticText(self.panel,-1,"主题:",pos=(x,60))
        self.subject=wx.TextCtrl(self.panel,-1,"",pos=(x,80),size=(380,25))
        self.content=wx.TextCtrl(self.panel,-1,"",pos=(x,110),size=(380,240),style=wx.TE_MULTILINE)
        self.sendBt=wx.Button(self.panel,-1,"发送",pos=(x,360),size=(50,30))
        self.addAttrBt=wx.Button(self.panel,-1,"添加附件",pos=(100,360),size=(80,30))
        self.Bind(wx.EVT_BUTTON,self.OnAdd,self.addAttrBt)
        wx.StaticText(self.panel,-1,"已添加附件:",pos=(400,10))
        self.attrListTE=wx.ListBox(self.panel,-1,pos=(400,30),size=(80,200))
        self.Bind(wx.EVT_LISTBOX_DCLICK,self.OnList,self.attrListTE)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.Bind(wx.EVT_BUTTON,self.OnSend,self.sendBt)
    
    def OnClose(self,event):
        print "Bye"
        self.Destroy()
        sys.exit()
        

    def OnList(self,event):
        posId=event.GetSelection()
        item=event.GetEventObject()
        self.attrList.remove(item.GetStringSelection())
        item.Delete(posId)

    def OnAdd(self,event):
        self.addAttr()
    
    def addAttr(self):
        wOpen=wx.FileDialog(self,message="请选择附件:",defaultDir=os.getcwd(),style=wx.OPEN)
        if wOpen.ShowModal() == wx.ID_OK:
            self.attrList.append(wOpen.GetPath())
            self.attrListTE.Append(wOpen.GetPath())
    
    def OnSend(self,event):
        threading.Thread(target=self.sendMail).start()

    def addFile(self,filePath,fileName):
        try:
            mainType,subType=mimetypes.guess_type()[0].split('/')
        except:
            mainType="application"
            subType="None"
        fd=open(filePath,"rb")
        if mainType=="text":
            msgAttr=MIMEText(fd.read())
        elif mainType=="image":
            msgAttr=MIMEImage(fd.read(),subType)
        elif mainType=="audio":
            msgAttr=MIMEAudio(fd.read(),subType)
        else:
            msgAttr=MIMEBase(mainType,subType)
            msgAttr.set_payload(fd.read())
            encode_base64(msgAttr)
        msgAttr["Content-Disposition"]="attachment;filename=%s" %fileName.encode('gbk')
        fd.close()
        return msgAttr


    def sendMail(self):
        to_list=self.toText.GetValue().split(';')
        msgRoot=MIMEMultipart()
        msgRoot["Subject"]=u"%s" %self.subject.GetValue()
        msgRoot["From"]=self.fromTo
        msgRoot["To"]=';'.join(to_list)
        msgText=MIMEText(u"%s"%self.content.GetValue(),_charset="utf8")
        msgRoot.attach(msgText)
        for filePath in self.attrList:
            msgRoot.attach(self.addFile(filePath,os.path.basename(filePath)))
        try:
            self.SetTitle("发送中...")
            self.smtp.sendmail(self.fromTo,to_list,msgRoot.as_string())
            WorkerThread(self,self.SetTitle,"发送成功").start()
        except:
            WorkerThread(self,self.SetTitle,"发送失败").start()
        

class loginFrame(wx.Frame):
    def __init__(self,userName='',passWord='',isCheck=''):
        wx.Frame.__init__(self,None,-1,"请登录您的邮箱",size=(300,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.panel=wx.Panel(self,-1)
        self.host=self.readHost()
        self.ShowElements(userName,passWord,isCheck)
        self.Center(True)
        self.Show()
    
    def readHost(self):
        try:
            db=openDb(Db)
            return db['host']
        except:
            return ['']
    def ShowElements(self,userName,passWord,isCheck):
        pos_x=10
        self.createMenu()
        wx.StaticText(self.panel,-1,"账号:",pos=(pos_x,20))
        wx.StaticText(self.panel,-1,"密码:",pos=(pos_x,60))
        self.messLabel=wx.StaticText(self.panel,-1,"",pos=(pos_x,150))

        self.userText=wx.TextCtrl(self.panel,-1,userName,pos=(50,15),size=(200,30))
        self.userText.SetFocus()
        self.pwdText=wx.TextCtrl(self.panel,-1,passWord,pos=(50,55),size=(200,30),style=wx.TE_PASSWORD)
        self.loginBt=wx.Button(self.panel,-1,'登录',pos=(50,110),size=(50,30))
        self.loginBt.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnLogin,self.loginBt)
        self.checkBox=wx.CheckBox(self.panel,-1,"记住密码",pos=(50,85))
        self.checkBox.SetValue(isCheck=='1')
        
    
    def OnLogin(self,event):
        re_email=re.compile(r'.+@(.+)') 
        user=self.userText.GetValue()
        pwd=self.pwdText.GetValue()
        emailAdd=re_email.match(user)
        if not (emailAdd and pwd):
            wx.MessageBox('账号或密码不可为空,且邮件格式要正确～',
                    '请检查')
            return 127
        self.changeLabel(self.messLabel,"登录中")
        threading.Thread(target=self.loginMail,args=(user,pwd,)).start()
        
    def getHost(self,user):
        return ["smtp." +  user[user.find('@')+1:]]

    def changeLabel(self,label,value):
        label.SetLabel(value)

    def loginMail(self,user,pwd):
        smtp=smtplib.SMTP()
        try:
            smtp.connect(*(self.host if  self.host[0] else self.getHost(user)))
            smtp.login(user,pwd)
            WorkerThread(self,self.changeLabel,self.messLabel,"登录成功").start()
            if self.checkBox.GetValue():
                saveInfo(userName=user,passWord=pwd,isCheck='1')
            else:
                saveInfo(userName='',passWord='',isCheck='')
            self.Show(False)
            wx.CallAfter(mailFrame,user,smtp)
        except smtplib.SMTPAuthenticationError:
            WorkerThread(self,self.changeLabel,self.messLabel,"用户名或密码出错").start()
            smtp.close()
            return 127
        except:
            WorkerThread(self,self.changeLabel,self.messLabel,"连接smtp服务器出错").start()
            return 127
            

    def createMenu(self):
        menuBar=wx.MenuBar()
        menu=wx.Menu()
        setHostItem=menu.Append(wx.NewId(),
                '设置smtp服务器','设置smtp服务器')
        self.Bind(wx.EVT_MENU,self.setHost,setHostItem)
        menuBar.Append(menu,'设置')
        self.SetMenuBar(menuBar)

    def setHost(self,event):
        mailHost=wx.GetTextFromUser("请输入smtp服务器地址\n\
                如果不是默认25端口,请在地址后跟\":+端口号\"",
                "需要自定义smtp地址吗?",
                ':'.join(self.host))
        self.host=mailHost.split(':')
        writeDb(openDb(Db),'host',self.host)
    
if __name__=='__main__':
    app=wx.App()
    login=loginFrame(**readInfo("userName","passWord","isCheck"))
    app.MainLoop()
