#!/usr/bin/env python
#coding:utf-8
import urllib,urllib2,cookielib,re,json,wx,thread,threading,time
loginPost={
        'staticpage':'http://fm.baidu.com/v3Jump.html',
        'charset':'utf8',
        'token':'',
        'tpl':'fm',
        'apiver':'v3',
        'safeflg':'0',
        'u':'http://fm.baidu.com',
        'isPhone':'false',
        'quick_user':'0',
        'logintype':'basicLogin',
        'username':'',
        'password':'',
        }
addPost={
        'method':'add_task',
        'app_id':'250528',
        'source_url':'',
        'save_path':'/downloads/',
        }
hds={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        }
loginUrl='https://passport.baidu.com/v2/api/?login'
class downFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'疯狂的离线下载(q8886888@qq.com)',size=(700,600),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.t_getPageData=threading.Thread(target=self.getPageData)
        self.t_getPageData.start()
        self.Center()
        self.panel=wx.Panel(self,-1)
        self.Show(True)
        self.ShowElement()
 #       self.showSpace()
        self.t_showSpace=threading.Thread(target=self.showSpace)
        self.t_showSpace.start()
        self.Bind(wx.EVT_LISTBOX_DCLICK,self.OnSpaceList,self.spaceList)
    def labelData(self):
        x=5
        return(
                ('用户:',(x,30)),
                ('容量:',(x,60)),
                ('添加下载:',(x,110)),
                ('下载列表:',(x,160)),
                ('离线空间:',(x,300)),
                ('',(x+40,30)),
                ('',(x+40,60)),
                )
    def createLabel(self):
        item=[]
        for data in self.labelData():
            item.append(wx.StaticText(self.panel,-1,label=data[0],pos=data[1]))
        self.userLabel=item[-2]
        self.spaceLabel=item[-1]
        
    def ShowElement(self):
        x=80
        width=500
        self.downText=wx.TextCtrl(self.panel,-1,"",pos=(x,100),size=(width,40))
        self.downList=wx.ListBox(self.panel,-1,pos=(x,160),size=(width,120))
        self.spaceList=wx.ListBox(self.panel,-1,pos=(x,300),size=(width,250))
        self.createButton()
        self.createLabel()
        self.showInfo()
    def createButton(self):
        for data in self.buttonData():
            self.Bind(wx.EVT_BUTTON,data[3],wx.Button(self.panel,-1,data[0],pos=data[1],size=data[2]))
    def buttonData(self):
        x=600
        return (
                ("添加任务",(x,100),(-1,40),self.OnAdd),
                ("刷新内容",(x,300),(-1,40),self.OnRefresh),
                ("下载文件",(x,350),(-1,40),self.OnDownFile),
                ("删除文件",(x,400),(-1,40),self.OnDelFile),
                )
    def OnRefresh(self,event):
        if len(self.spaceItem):threading.Thread(target=self.showSpace).start()

    def OnDownFile(self,event):
        pass
    def OnDelFile(self,event):
        pass
    def OnAdd(self,event):
        for url in self.downText.GetValue().encode('utf8').split(";",10):
           # self.addTask(url)
            threading.Thread(target=self.addTask,args=(url,)).start()
    def addTask(self,url):
        
        addPost['source_url']=url
        addData=urllib.urlencode(addPost)
        req=urllib2.Request(self.addUrl,addData,hds)
        try:
            print urllib2.urlopen(req).read()
        except urllib2.HTTPError,e:
            print e
    
    def showInfo(self):
        self.t_getPageData.join()
        self.userLabel.SetLabel(self.uid)
        self.spaceLabel.SetLabel(self.space)
    def showSpace(self):
        #req=urllib2.Request(spaceUrl)
        self.spaceList.Clear()
        page=urllib2.urlopen(self.spaceUrl).read()
        text=json.loads(page)['list']
        text.reverse()
        self.spaceItem=text
        for data in self.spaceItem:
            self.spaceList.Append(data['server_filename'] + "--size:" + str(round(float(data['size'])/1024/1024.0,2)) + "MB,time:" +time.strftime("%Y-%m-%d %T",time.localtime(data['server_mtime'])))

    def OnSpaceList(self,event):
        Id=self.spaceList.GetSelection()
        data=self.spaceItem[Id]
        mess='文件名:%s\n大小:%s \n时间:%s \n文件被修改时间:%s\nmd5:%s'%(data['server_filename'].encode('utf8'),str(round(float(data['size'])/1024/1024.0,2))+'MB',self.strTime(data['server_mtime']),self.strTime(data['local_mtime']),data['md5'].encode('utf8'))
        wx.MessageDialog(self.panel,mess,'文件详情',style=(wx.OK)).ShowModal()
    def strTime(self,t):
        return time.strftime("%Y-%m-%d %T",time.localtime(t))
    def getPageData(self):
        page=urllib2.urlopen('http://pan.baidu.com').read()
        re_bdstoken=re.compile(r'FileUtils\.bdstoken=\"(.+?)\"')
        re_uid=re.compile(ur'FileUtils\.sysUID=\"(.*?)\"')
        re_space=re.compile(r'<span id=\"remainingSpace\">(.+?)</div>',re.S)
        self.uid=re_uid.findall(page)[0]
        self.bdstoken=re_bdstoken.findall(page)[0]
        self.space=re_space.findall(page)[0]
        self.space=re.sub(r'</?span>','',self.space)
        self.spaceUrl="http://pan.baidu.com/api/list?channel=chunlei&clienttype=0&web=1&num=100&page=1%&dir=%2Fdownloads&order=time"+"&bdstoken=%s&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
        self.addUrl="http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=%s&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
class loginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'请登录你的百度',size=(350,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.Center()
        self.panel=wx.Panel(self,-1)
        userLabel=wx.StaticText(self.panel,-1,'账号: ',pos=(10,30),size=(50,-1))
        pwdLabel=wx.StaticText(self.panel,-1,'密码: ',pos=(10,60),size=(50,-1))
        self.userText=wx.TextCtrl(self.panel,-1,'',pos=(userLabel.GetSize()[0],30),size=(150,-1))
        self.pwdText=wx.TextCtrl(self.panel,-1,'',pos=(userLabel.GetSize()[0],60),size=(150,-1),style=wx.TE_PASSWORD)
        self.userText.SetFocus()
        self.checkText=wx.TextCtrl(self.panel,-1,"",pos=(240,60))
        self.checkLabel=wx.StaticText(self.panel,-1,"↑验证码↑",pos=(240,90))
        self.checkText.Show(False)
        self.checkLabel.Show(False)
        self.messLabel=wx.StaticText(self.panel,-1,"",pos=(30,150))
        self.button=wx.Button(self.panel,-1,"登录",pos=(30,120))
        self.button.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.button)
        self.Show(True)
        self.bd=baidu()
        self.bd.initData()
    def OnClick(self,event):
        self.bd.t.join()
        if self.checkText.IsShown():self.setCode()
        user=self.userText.GetValue().encode('utf8')
        pwd=self.pwdText.GetValue().encode('utf8')
        loginPost['username']=user
        loginPost['password']=pwd
        if self.bd.sendPost():
            self.messLabel.SetLabel("登录成功")
            self.Show(False)
            downFrame()
        else:
            self.showCode()
            self.messLabel.SetLabel("登录失败，请检查！")
            self.checkText.SetFocus()
       # loginPost['verifycode']=checkCode
    def showCode(self):
        if self.bd.getCode():
            img=wx.Image('/data/_baidu.gif',wx.BITMAP_TYPE_ANY)
            self.checkText.Show(True)
            self.checkLabel.Show(True)
            self.checkCodeImg=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(img),pos=(240,20))
    def setCode(self):
        loginPost['verifycode']=self.checkText.GetValue()
class baidu():
    def initData(self):
      self.t=threading.Thread(target=self.getToken,args=('http://www.baidu.com','http://passport.baidu.com/v2/api/?getapi&tpl=fm',))
      self.t.start()
    def getToken(self,url1,url2):
        urllib2.urlopen(url1)
        re_token=re.compile('_token=\'(.+?)\'')
        token=re_token.findall(urllib2.urlopen(url2).read())[0]
        print token
        loginPost['token']=token

    def getCode(self):
        try:
            loginPost['codestring']=self.codeStr
            imgUrl='https://passport.baidu.com/cgi-bin/genimage?' + self.codeStr
            urllib.urlretrieve(imgUrl,'/data/_baidu.gif')
            return True
        except Exception:
            pass
            return False
       # self.sendPost()
    def sendPost(self):
        data=urllib.urlencode(loginPost)
        result=urllib2.Request(loginUrl,data,hds)
        text=urllib2.urlopen(result).read()
        re_codeStr=re.compile(r'codeString=(.*?)&')
        re_no=re.compile(r'err_no=(.*?)&')
        self.codeStr=re_codeStr.findall(text)[0]
        if  int(re_no.findall(text)[0])==0:
            return True
        else:
            return False
        #print self.codeStr
        
if __name__=='__main__':
    cj=cookielib.LWPCookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    mutex=threading.Lock()
    app=wx.App()
    lFrame=loginFrame()
    app.MainLoop()
  #  bd=baidu()
  #  bd.login('q8886888@qq.com','zxc123')

    

