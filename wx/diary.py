#coding:utf8
import hashlib
import webbrowser
import wx
import time
import os
import re
import sys
import shelve
import threading
import urllib
from qiniu import conf,rs,io

"""
    isKeyTrue(userpass)函数用来验证密码是否正确
    OnGet()是单击ListCtrl项时触发的事件，用来取得Text，得到字典key
    md5UserPass(userPass)返回一个经MD5加密的密码
    diaryList 这是日记列表的控件,diariesList 存的是日志列表，不要弄混
    listDiaries()是用来显示列表的函数
    
"""
Db=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'userData.db')
ZONENAME="ljd-dbdata"
DOMAIN="ljd-dbdata.qiniudn.com"

def openDb(dbUrl):
    return shelve.open(dbUrl,'c')

def readKey():
    db=openDb(Db)
    try:
        return  'password'  in db
    finally:
        db.close()

def setKey(userPass):
    userPass=md5UserPass(userPass)
    db=openDb(Db)
    if 'password' not in db:
        db['password']=userPass
    else:
        oldPass=md5UserPass(wx.GetTextFromUser('为了验证用户的真实性,请输入旧密码来确认修改密码权限','验证旧密码'))
        if db['password'] ==oldPass:
            db['password']=userPass
            return True
        else:
            return False
    db.close()
    return True

def delKey():
    db=openDb(Db)
    del db['password']
    db.close()

def md5UserPass(userPass):
    md5Pass=hashlib.md5()
    md5Pass.update(userPass)
    return md5Pass.hexdigest()

class contentFrame(wx.MiniFrame):
    def __init__(self,window,title,content):
        print title
        wx.MiniFrame.__init__(self,window,-1,title=u'%s写的日记'%title,size=(400,300),style=wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT)
        self.Show()
        self.Center()

class KeyFrame():
    def __init__(self):
        password=wx.GetPasswordFromUser('请输入日记本启动密码','日记本已加密')
        if (not  password) or (not self.isKeyTrue(password)):
            wx.MessageBox('打开日记本出错了吧！','出错了吧,嘻嘻')
            sys.exit()
        diaryFrame=DiaryFrame()
    def isKeyTrue(self,userpass):
        db=openDb(Db)
        userpass=md5UserPass(userpass)
        return db['password'] == userpass
        
    
class qiniuDo():
    def __init__(self,window):
        conf.ACCESS_KEY="BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm"
        conf.SECRET_KEY="WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs"
        self.policy=rs.PutPolicy(ZONENAME)
        self.token=self.policy.token()
        self.window=window
        self.filename=os.path.basename(Db).strip()

    def putData(self):
        import socket
        socket.setdefaulttimeout(3)
        try:
            ret,err=io.put_file(self.token,self.filename,Db)
            if err:
                rs.Client().delete(ZONENAME,self.filename)
                self.putData()
            else:
                wx.CallAfter(self.showMsg,"数据库上传成功")
        except:
            wx.CallAfter(self.showMsg,"数据库上传失败")

    def showMsg(self,msg):
        wx.MessageBox('%s'%msg,'提示',wx.OK)
        
    
    def put(self):
        t=threading.Thread(target=self.putData)
        t.start()
    
    def getData(self):
        url=rs.make_base_url(DOMAIN,self.filename)
        policy=rs.GetPolicy()
        private_url=policy.make_request(url)
        try:
            urllib.urlretrieve(private_url,Db)
        except:
            wx.CallAfter(self.showMsg,"数据库下载失败")
        wx.CallAfter(self.window.listDiaries)
        wx.CallAfter(self.showMsg,"数据库下载成功")
        
            
    
    def get(self):
        t=threading.Thread(target=self.getData)
        t.start()



class DiaryFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'今天是%s,请写下今天的日记~'
                
                %reduce(lambda x,y:x+y ,[x+y for x,y in zip(time.strftime('%Y %m %d',time.localtime()).split(), ['年','月','日'] )]),
                size=(600,600),
                style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.pan=qiniuDo(self)
        self.isOpen=False
        self.showElement()
        self.timer=wx.Timer(self,-1)
        self.Bind(wx.EVT_TIMER,self.OnTimer,self.timer)
        self.timer.Start(1000)
        self.Center()
        self.Show()
    def OnTimer(self,event):
        self.changeTime()
    def changeTime(self):
        self.timeLabel.SetLabel(time.asctime())

    def showElement(self):
        x=10
        self.panel=wx.Panel(self,-1)
        self.createMenuBar()
        self.diaryList=wx.ListCtrl(self.panel,-1,style=wx.LC_REPORT,pos=(x,10),size=(500,250))
        map(lambda x,i:self.diaryList.InsertColumn(i,x),('时间','日记'),range(2))
        self.diaryList.SetColumnWidth(0,150)
        self.diaryList.SetColumnWidth(1,350)
        self.diaryList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnGet)
        self.diaryList.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.OnLook)
        self.contentText=wx.TextCtrl(self.panel,-1,'',pos=(-1,300),size=(600,280),style=wx.TE_MULTILINE)
        self.createButton()
        self.listDiaries()
        wx.StaticText(self.panel,-1,'现在是:',pos=(-1,270))
        self.timeLabel=wx.StaticText(self.panel,-1,time.asctime(),pos=(50,270))
        
    def buttonData(self):
        return (
                ('查看日记',(75,-1),(520,10),self.OnLook),
                ('保存日记',(75,-1),(520,50),self.OnSave),
                ('删除日记',(75,-1),(520,90),self.OnDel),
                ('新写日记',(75,-1),(520,130),self.OnNew),
                )

    def OnGet(self,event):
        self.selectItem=event.GetText()

    def OnDel(self,event):
        self.delDiary()
    
    def OnNew(self,event):
        self.newDiary()
    
    def newDiary(self):
        self.contentText.Clear()
        self.isOpen=False

    def delDiary(self):
        del self.diariesList[self.selectItem]
        self.saveDb()
        self.listDiaries()


    def createButton(self):
        for label,size,pos,handle in self.buttonData():
            butItem=wx.Button(self.panel,-1,label=label,size=size,pos=pos)
            self.Bind(wx.EVT_BUTTON,handle,butItem)
    def OnLook(self,event):
        self.lookContent()
    def lookContent(self):
        self.isOpen=True
        self.contentText.SetValue(self.diariesList[self.selectItem])

    def listDiaries(self):
        self.diaryList.DeleteAllItems()
        db=openDb(Db)
        if 'diaries' not in db:
            self.diariesList={}
            return False
        self.diariesList=db['diaries']
        for changeTime in self.diariesList:
            titleData=self.diariesList[changeTime]
            En=titleData.find('\n')
            title=titleData[:En] if 0<En < 60 else titleData[0:60]
            self.diaryList.InsertStringItem(0,changeTime)
            self.diaryList.SetStringItem(0,1,title)

    def OnSave(self,event):
        if not self.contentText.GetValue().strip():
            wx.MessageBox('请不要保存空日记，好吗？','保存失败',wx.OK)
            return False
        self.saveContent()

    def saveContent(self):
        diary=self.contentText.GetValue()
        if not self.isOpen:
            nowTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        else:
            nowTime=self.selectItem
        self.diariesList[nowTime]=diary
        self.saveDb()
        self.listDiaries()
        self.isOpen=False
        self.contentText.Clear()
    def saveDb(self):
        db=openDb(Db)
        db['diaries']=self.diariesList
        db.close()
        

    def menuData(self):
        return (
                ('操作',
                    ('新建日记\tCtrl-N','',self.OnNew),
                    ('保存日记\tCtrl-S','保存现在正在写的日记!',self.OnSave),
                    ('设置密码','设置一个日记本启动密码',self.OnSetKey),
                    ('插入日期','year-mon-day',self.OnInsertData),
                    ('删除密码','删除日记本启动密码',self.OnDelKey),
                ),
                ('关于',
                    ('访问作者','',self.OnToMe),
                    ),
                ('数据同步',
                    ('上传数据','',self.OnUp),
                    ('下载数据','',self.OnDown),
                    ),
                )
    
    def OnUp(self,event):
        self.pan.put()
    def OnDown(self,event):
        self.pan.get()

    def OnInsertData(self,event):
        date=time.strftime("%Y-%m-%d")
        self.contentText.AppendText(date)

    
    def createMenuBar(self):
        self.menuItem=[]
        self.menuBar=wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel=eachMenuData[0]
            menuItems=eachMenuData[1:]
            self.menuBar.Append(self.createMenu(menuItems),menuLabel)
        self.SetMenuBar(self.menuBar)
        self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('N'),self.menuItem[0].GetId())]))
        self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('S'),self.menuItem[1].GetId())]))
        self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('I'),self.menuItem[3].GetId())]))
        
    def OnToMe(self,event):
        webbrowser.open_new_tab('http://linux.zj.cn')
    def createMenu(self,menuItems):
        menu=wx.Menu()
        for label,status,handle in menuItems:
            item=menu.Append(wx.NewId(),label,status)
            self.Bind(wx.EVT_MENU,handle,item)
            self.menuItem.append(item)
        return menu
    
    def OnSetKey(self,event):
        userPass=wx.GetTextFromUser('请输入日记启动密码','请输入密码')
        if re.match(r'\s',userPass) and userPass:
            wx.MessageBox('密码中不可以加空格哦~','密码中有空格',wx.OK)
            return False
        if userPass and ( not  setKey(userPass)):
            wx.MessageBox('旧密码不正确','密码修改错误')
    def OnDelKey(self,event):
        delKey()
        
if __name__=='__main__':
    app=wx.App()
    if not readKey():
        frame=DiaryFrame()
    else:
        keyFrame=KeyFrame()
    app.MainLoop()
