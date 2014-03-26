#coding:utf8
import re
import wx
import shelve
import os
import threading
import sys
import smtplib

Db=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"mail.db")

def openDb(dbUrl):
    return shelve.open(dbUrl,'c')
def writeDb(db,key,value):
    db[key]=value
    db.close()
class WorkerThread(threading.Thread):
    def __init__(self,window,fun,*args):
        threading.Thread.__init__(self)
        self.window=window
        self.fun=fun
        self.args=args
    def run(self):
        wx.CallAfter(self.fun,*args)

class mailFrame(wx.Frame):
    def __init__(self,myEmail):
        wx.Frame.__init__(self,None,-1,myEmail,size=(500,400),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.panel=wx.Panel(self,-1)
        self.ShowElements()
        self.Center()
        self.Show()

class loginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"请登录您的邮箱",size=(300,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.panel=wx.Panel(self,-1)
        self.host=self.readHost()
        self.ShowElements()
        self.Center(True)
        self.Show()
    
    def readHost(self):
        try:
            db=openDb(Db)
            return db['host']
        except:
            return ['']
    def ShowElements(self):
        pos_x=10
        self.createMenu()
        wx.StaticText(self.panel,-1,"账号:",pos=(pos_x,20))
        wx.StaticText(self.panel,-1,"密码:",pos=(pos_x,60))
        self.messLabel=wx.StaticText(self.panel,-1,"",pos=(pos_x,150))

        self.userText=wx.TextCtrl(self.panel,-1,'',pos=(50,15),size=(200,30))
        self.userText.SetFocus()
        self.pwdText=wx.TextCtrl(self.panel,-1,'',pos=(50,55),size=(200,30),style=wx.TE_PASSWORD)
        self.loginBt=wx.Button(self.panel,-1,'登录',pos=(50,100),size=(50,30))
        self.loginBt.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnLogin,self.loginBt)
    
    def OnLogin(self,event):
        re_email=re.compile(r'.+@(.+)') 
        user=self.userText.GetValue()
        pwd=self.pwdText.GetValue()
        emailAdd=re_email.match(user)
        if not (emailAdd and pwd):
            wx.MessageBox('账号或密码不可为空,且邮件格式要正确～',
                    '请检查')
            return 127
        self.messLabel.SetLabel('登录中...')
        self.loginMail(user,pwd)
        mailFrame(user)
        
    def loginMail(self,user,pwd):
        pass

    def createMenu(self):
        menuBar=wx.MenuBar()
        menu=wx.Menu()
        setHostItem=menu.Append(wx.NewId(),
                '设置smtp服务器','设置smtp服务器')
        self.Bind(wx.EVT_MENU,self.setHost,setHostItem)
        menuBar.Append(menu,'设置')
        self.SetMenuBar(menuBar)

    def setHost(self,event):
        mailHost=wx.GetTextFromUser("请输入smtp服务器地址\n
                如果不是默认25端口,请在地址后跟\":+端口号\"",
                "需要自定义smtp地址吗?",
                ':'.join(self.host))
        self.host=mailHost.split(':')
        writeDb(openDb(Db),'host',self.host)
if __name__=='__main__':
    app=wx.App()
    login=loginFrame()
    app.MainLoop()
