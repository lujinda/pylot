#!/usr/bin/env python
#coding:utf-8
"""
部分函数／事件说明：
OnKey,接收键盘d事件，下载文件
getTaskId，获取所有的任务id,前后两个任务id，用%连起
ShowElement 显示出各种控件元素
OnSwit 将迅雷，快车，旋风地址解密
self.addUrl,self.delUrl,self.uid,self.bdstoken,self.space ,分别是添加任务地址，删除任务地址，用户名，百度网盘的token，容量
使用重构的方式创建菜单，wx.EVT_MENU的GetEventObject获取到的是Menu类型的对象，所以我使用self.MenuBar.FindITemById(event.GetId())来查找我点击的MenuItem
swTop()用来设置是否窗口置顶，setTimer()用来设置刷新时间（秒）,offTimer()用来关闭和开启自动刷新,self.secTimer变量存储了自动更新的时间
self.showDownPro()用来显示下载进度条
self.startDown()是真正下载文件用的
readDb()是用来读取数据库文件的，里面会记录着用户名和密码，还有是否要记录密码选项
writeDb()是用来写入数据库的。
loginBd()登录百度
autoLogin()自动登录用的
"""
import urllib
import urllib2
import cookielib
import re
import inspect
import json
import wx
import thread
import threading
import time
import webbrowser
import base64
import sys
import os
import mimetypes
import shelve
import tempfile
dbUrl=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'.pan.db')
cjUrl=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'._cj_ljd.txt')
TempCodeImg=tempfile.mkstemp()[1]+'.gif'
RemoteDir='/downloads/'
Time=5000
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
        'mem_pass':'on',
        'username':'',
        'password':'',
        }
delPost={
        'filelist':''
        }
qdPost={
        'ie':'utf-8',
        'kw':'',
        'tbs':'',
        }
mkPost={
        'path':'',
        'isdir':'1',
        'method':'post',
        'block_list':'[]',
        'size':'',
        }

addPost={
        'method':'add_task',
        'app_id':'250528',
        'source_url':'',
        'save_path':RemoteDir,
        }
hds={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Referer':'http://pan.baidu.com/disk/home',
        }
tbHds={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Referer':'http://tieba.baidu.com/'
        }
loginUrl='https://passport.baidu.com/v2/api/?login'

def writeDb(**kwargs):
    db=shelve.open(dbUrl,'c')
    for key in kwargs:
        db[key]=kwargs[key]
    db.close()
def readDb(*args):
    db=shelve.open(dbUrl,'c')
    d={}
    for key in args:
        try:
            d[key]=db[key]
        except:
            d[key]=''
            break
    db.close()
    return d
    

class WorkerThread(threading.Thread):
    def __init__(self,window,fun):
        threading.Thread.__init__(self)
        self.window=window
        self.fun=fun
        self.timeToQuit=threading.Event()
        self.timeToQuit.clear()
    def run(self):
        wx.CallAfter(self.fun)
class downFrame(wx.Frame):
    def __init__(self,Parent):
        wx.Frame.__init__(self,Parent,-1,'下载管理器',
                size=(600,400),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.Center()
        self.Show()

class panFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'疯狂的离线下载(q8886888@qq.com)',
                size=(700,600),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.t_getPageData=threading.Thread(target=self.getPageData)
        self.t_getPageData.start()
        self.Center()
        self.panel=wx.Panel(self,-1)
        self.Show(True)
        self.ShowElement()
        self.getSpace()
        self.Iden=False
        self.getDown()
        self.downItem={}
        self.timer=wx.Timer(self,-1)
        self.secTimer=10000
        self.timer.Start(self.secTimer)
        self.Bind(wx.EVT_TIMER,self.OnTimer,self.timer)
        self.Bind(wx.EVT_KEY_UP,self.OnKey)
        #self.t_showSpace.start()

    def OnAddQd(self,event):
        threading.Thread(target=self.addQd).start()
        wx.MessageBox('一键签到已开始，稍等一会见结果\n如果有疑问请Q:929300079','签到开始了!')
    def addQd(self):
        url='http://tieba.baidu.com/sign/add'
        qdResult={}
        for kwUrl,kw in self.getKw():
            kwUrl='http://tieba.baidu.com' + kwUrl
            kw=unicode(kw,'gbk').encode('utf8')
            qdPost['kw']=kw
            qdPost['tbs']=self.getTbs('http://tieba.baidu.com/f?kw=%s&fr=index'%kw)
            qdData=urllib.urlencode(qdPost)
            req=urllib2.Request(url,qdData,tbHds)
            error=json.loads(urllib2.urlopen(req).read())['error']
            qdResult[kw]=error or u'签到成功'
        self.qdEnd(qdResult)
    def qdEnd(self,result):
        mess=''
        for kw in result:
            mess=mess + '%s : %s\n'%(kw,result[kw].encode('utf8'))
        wx.CallAfter(wx.MessageBox,mess,'签到已完成')

    def getKw(self):
        tbUrl='http://tieba.baidu.com/f/like/mylike'
        page=urllib2.urlopen(tbUrl).read()
        re_kw=re.compile(r'<a href=\"(.+?)\" title=\"(.+?)\">')
        return re_kw.findall(page)
    def getTbs(self,url):
        re_tbs=re.compile(r'PageData.tbs = \"(.+?)\"')
        page=urllib2.urlopen(url).read()
        return re_tbs.findall(page)[0]

    def OnKey(self,event):
        kc=event.GetKeyCode()
        if self.spaceList.GetSelection >=0 and kc==68:
            WorkerThread(self,self.downFile).start()
        if kc==344 and self.buttonItem[2].IsEnabled():
            self.buttonEnable(False)
            self.refresh()
    def buttonEnable(self,Bool):
        for i in range(0,5):
            self.buttonItem[i].Enable(Bool)
    def OnDelFile(self,event):
        Id=self.spaceList.GetSelection()
        if Id >=0:
            self.SetTitle('删除中....')
            threading.Thread(target=self.delFile,args=([self.spaceItem[Id],],)).start()
    def OnDelAllFile(self,event):
        self.SetTitle('删除中....')
        if self.spaceList.GetSelection >=0:threading.Thread(target=self.delFile,args=(self.spaceItem,)).start()
    
    def delFile(self,Item):
        self.buttonEnable(False)
        fileNames=[]
        for data in Item:
            fileNames.append(data['path'].encode('utf8'))
        delPost['filelist']=fileNames
        data=urllib.urlencode(delPost)
        data=data.replace('%27','%22')
        data=data.replace('%5Cx','%')
        #data=data.replace('\[\"','%5B%22')
        #data=data.replace('\]\"','%5D%22')
       # data=data.replace('/','%2F')
        req=urllib2.Request(self.delUrl,data,hds)
        result=json.loads(urllib2.urlopen(req).read())
        print result
        if result['errno'] ==0:
            self.SetTitle('删除成功')
            threading.Thread(target=self.getSpace).start()
        else:
            self.SetTitle('删除失败')
    def labelData(self):
        x=5
        return(
                ('用户:',(x,10)),
                ('容量:',(x,40)),
                ('添加下载:',(x,90)),
                ('地址转换:',(x,140)),
                ('下载列表:',(x,190)),
                ('离线空间:',(x,300)),
                ('',(x+40,10)),
                ('',(x+40,40)),
                )
    def createLabel(self):
        item=[]
        for data in self.labelData():
            item.append(wx.StaticText(self.panel,-1,label=data[0],pos=data[1]))
        self.spaceSizeLabel=item[1]
        self.userLabel=item[-2]
        self.spaceLabel=item[-1]
        
    def menuData(self):
        return (
                ('设置',
                    ('设置刷新时间\tCtrl-t','设置自动刷新时间',self.setTimer),
                    ('关闭自动刷新\t','关闭刷新功能',self.offTimer),
                    ('关闭自动登录\t','关闭自动登录功能',self.offAuto),
                    ),
                )
    def createMenu(self):
        menuBar=wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel=eachMenuData[0]
            menuItems=eachMenuData[1:]
            menuBar.Append(self.createMenuItem(menuItems),menuLabel)
        self.SetMenuBar(menuBar)
    def createMenuItem(self,eachData):
        menu=wx.Menu()
        for label,status,handler in eachData:
            item=menu.Append(wx.NewId(),label,status)
            if label[-1].isalpha():
                ctrl=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord(label[-1]),item.GetId())])
                self.SetAcceleratorTable(ctrl)
            self.Bind(wx.EVT_MENU,handler,item)
        return menu

    def offAuto(self,event):
        writeDb(isAuto=False)

    def ShowElement(self):
        x=80
        width=500
        self.createMenu()
        self.downText=wx.TextCtrl(self.panel,-1,"",pos=(x,80),size=(width,40))
        self.switText=wx.TextCtrl(self.panel,-1,"",pos=(x,130),size=(width,40))
        self.downList=wx.ListCtrl(self,-1,style=wx.LC_REPORT,pos=(x,190),size=(width,100))
        isTop=wx.CheckBox(self.panel,-1,'窗口保持最前',pos=(5,570))
        self.Bind(wx.EVT_CHECKBOX,self.swTop,isTop)
        i=0
        for data in ('任务ID','文件名','下载进度','创建时间','源链接'):
            self.downList.InsertColumn(i,data)
            i+=1
        self.downList.SetColumnWidth(1,250)
        self.downList.SetColumnWidth(4,300)
        self.downList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnLeftClick)
        self.downList.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.OnDclick)
        self.spaceList=wx.ListBox(self.panel,-1,pos=(x,300),size=(width,250))
        self.checkText=wx.TextCtrl(self.panel,-1,"",pos=(x+150,30),size=(-1,-1))
        self.checkLabel=wx.StaticText(self.panel,-1,"请输入验证码:",pos=(x+150,10))
        self.offShow()
        self.createButton()
        self.createLabel()
        self.Bind(wx.EVT_LISTBOX_DCLICK,self.OnSpaceList,self.spaceList)
        self.spaceList.Bind(wx.EVT_KEY_UP,self.OnKey,self.spaceList)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.showInfo()
    def swTop(self,event):
        if event.GetEventObject().GetValue():
            self.SetWindowStyle(self.GetWindowStyle()|wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(self.GetWindowStyle() ^wx.STAY_ON_TOP)

    def OnTimer(self,event):
        self.refresh()
    def setTimer(self,event):
        dialog=wx.GetNumberFromUser(message='请输入一个5到6000之间的秒数\n(如果网络环境不好，请设置长一点)',
                prompt='秒数:',caption='设置自动刷新时间',value=self.secTimer/1000,min=5,max=6000,parent=None)
        if 10<=dialog<=6000 :
            self.secTimer=dialog*1000
            if self.timer.IsRunning():self.timer.Start(self.secTimer)
    def offTimer(self,event):
        item=self.MenuBar.FindItemById(event.GetId())
        if self.timer.IsRunning():
            self.timer.Stop()
            item.SetItemLabel('开启自动刷新')
        else:
            self.timer.Start(self.secTimer)
            item.SetItemLabel('关闭自动刷新')


       
    def OnLeftClick(self,event):
        pass

    def OnDclick(self,event):
        self.cancelUrl='http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=%s&task_id=%s&method=cancel_task&app_id=250528&channel=chunlei&clienttype=0&web=1' %(self.bdstoken,event.GetText())
        self.SetTitle('任务正在删除')
        self.downList.DeleteAllItems()
        threading.Thread(target=self.cancelTask).start()
    def cancelTask(self):
        urllib2.urlopen(self.cancelUrl)
        threading.Thread(target=self.getDown).start()
    def OnClose(self,event):
        self.Destroy() 
        sys.exit()
    def getDown(self):
        DownUrl='http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=%s&task_ids=%s&op_type=1&method=query_task&app_id=250528&channel=chunlei&clienttype=0&web=1' %(self.bdstoken,self.getTaskId())
        try:
            page=json.loads(urllib2.urlopen(DownUrl).read())['task_info']
            self.downPage=page
            WorkerThread(self,self.showDown).start()
        except urllib2.HTTPError,e:
                #self.showSpace()
                if self.downList.GetItemCount()==0:
                    print 'empty'
                    if self.Iden:
                        threading.Thread(target=self.getSpace).start()
                    self.Iden=False
                else:
                    pass
                    #threading.Thread(target=self.getDown).start()
                return False
    def showDown(self):
        line=0
        try:
            for data in self.downPage:
                item=self.downPage[data]
                self.downList.InsertStringItem(line,data)
                p=float(item['finished_size'])  / (float(item['file_size'])+1)
                self.downList.SetStringItem(line,1,item['task_name'].encode('utf8'))
                self.downList.SetStringItem(line,2,format(p,"0.2%"))
                self.downList.SetStringItem(line,3,self.strTime(float(item['create_time'])))
                self.downList.SetStringItem(line,4,item['source_url'].encode('utf8'))
                line+=1
            self.SetTitle('任务已刷新')       
        except Exception,e:
                print e
                threading.Thread(target=self.getDown).start()
        try:
            if self.lastTask>line:
                threading.Thread(target=self.getDown).start()
        except:
            pass
        self.lastTask=line
        self.buttonEnable(True)
    def getTaskId(self):
        page=urllib2.urlopen(self.taskIdUrl).read()
        text=json.loads(page)['task_info']
        taskId=""
        for data in text:
            taskId=taskId+','+ data['task_id']
        return urllib.quote(taskId[1:])
    def createButton(self):
        qdButton=wx.Button(self.panel,-1,'贴吧一键签到',pos=(200,10),size=(-1,-1))
        ctrl=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('Q'),qdButton.GetId())])
        self.SetAcceleratorTable(ctrl)
        self.Bind(wx.EVT_BUTTON,self.OnAddQd,qdButton)
        self.buttonItem=[]
        for data in self.buttonData():
            item=wx.Button(self.panel,-1,data[0],pos=data[1],size=data[2])
            self.buttonItem.append(item)
            self.Bind(wx.EVT_BUTTON,data[3],item)
        self.buttonItem[0].SetDefault()
    def buttonData(self):
        x=600
        return (
                ("添加任务",(x,80),(-1,40),self.OnAdd),
                ("转换地址",(x,130),(-1,40),self.OnSwit),
                ("刷新内容",(x,300),(-1,40),self.OnRefresh),
                ("删除文件",(x,350),(-1,40),self.OnDelFile),
                ("删除所有",(x,400),(-1,40),self.OnDelAllFile),
                ("下载文件",(x,450),(-1,40),self.OnDown),
                )
    def getMimeType(self,path):
        type=mimetypes.guess_type(path)[0]
        if not type:
            return 'application/octet-stream'
        else:
            return type
    def OnDown(self,event):
        WorkerThread(self,self.downFile).start()
        
    def selectFile(self):
        fileDialog=wx.FileDialog(self,message='请选择一个要上传的文件',defaultDir=os.getcwd(),style=wx.OPEN)
        if fileDialog.ShowModal()==wx.ID_OK:
            path=fileDialog.GetPath()
            return path 
    def OnRefresh(self,event):
        self.refresh()
        #self.showSpace()
    def refresh(self):
        self.buttonEnable(False)
        self.downList.DeleteAllItems()
        threading.Thread(target=self.getSpace).start()
        threading.Thread(target=self.getDown).start()
    def OnSwit(self,event):
        url=self.switText.GetValue().encode('utf8')
        if url.lower().startswith('thunder://'):
            url=base64.decodestring(url[10:])
            url=url[2:-2]
        elif url.lower().startswith('flashget://'):
            url=base64.decodestring(url[11:url.find('&')])
            url=url[10:-10]
        elif url.lower().startswith('qqdl://'):
            url=base64.decodestring(url[7:])
        else:
            url=""
            self.SetTitle('需要转换的地址不是迅雷,快车,旋风中的一个,请检查!')
        self.downText.Clear()
        self.downText.SetValue(url)

    def OnAdd(self,event):
        url=self.downText.GetValue().encode('utf8')
        if url:
            self.addTask(url)
    def onShow(self):
        self.checkText.Show(True)
        self.checkText.SetFocus()
        self.checkLabel.Show(True)
    def offShow(self):
        self.checkText.Show(False)
        self.checkLabel.Show(False)
    def addTask(self,url):
        self.switText.Clear()
        if self.checkText.IsShown():addPost['input']=self.checkText.GetValue()
        addPost['source_url']=url
        addData=urllib.urlencode(addPost)
        req=urllib2.Request(self.addUrl,addData,hds)
        try:
            page=json.loads(urllib2.urlopen(req).read())
            self.offShow()
            self.SetTitle('离线任务添加成功')
            self.Iden=True
            self.refresh()
        except urllib2.HTTPError,e:
            page=json.loads(e.read())
            self.SetTitle(page['error_msg'])
            if e.code==403:
                self.checkText.Clear()
                addPost['vcode']=page['vcode']
                self.getCode(page['img'])
    def getCode(self,url):
        urllib.urlretrieve(url,TempCodeImg)
        self.showCode()
    def showCode(self):
        img=wx.Image(TempCodeImg,wx.BITMAP_TYPE_ANY)
        self.checkCodeImg=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(img),pos=(320,30))
        self.onShow()
        os.remove(TempCodeImg)

    def showInfo(self):
        self.t_getPageData.join()
        self.userLabel.SetLabel(self.uid)
        self.getSpaceSize()
    def showSpaceSize(self):
        self.spaceLabel.SetLabel(self.spaceSize)
    def getSpace(self):
        page=urllib2.urlopen(self.spaceUrl).read()
        text=json.loads(page)
        errno=int(text['errno'])
        if errno:self.mkdir('/downloads')
        fileText=text['list']
        fileText.reverse()
        self.spaceItem=fileText
        WorkerThread(self,self.showSpace).start()
        threading.Thread(target=self.getSpaceSize).start()
    def mkdir(self,path):
        mkUrl='http://pan.baidu.com/api/create?a=commit&channel=chunlei&clienttype=0&web=1&bdstoken=%s'%self.bdstoken
        mkPost['path']=path
        mkData=urllib.urlencode(mkPost)
        req=urllib2.Request(mkUrl,mkData,hds)
        urllib2.urlopen(req)
    

    def showSpace(self):
        self.spaceList.Clear()
        for data in self.spaceItem:
            self.spaceList.Append(data['server_filename'] + "--size:" + str(round(float(data['size'])/1024/1024.0,2)) + "MB,time:" +time.strftime("%Y-%m-%d %T",time.localtime(data['server_mtime'])))
        self.buttonEnable(True)
        self.SetTitle('内容已刷新')
    def OnSpaceList(self,event):
        Id=self.spaceList.GetSelection()
        data=self.spaceItem[Id]
        mess='文件名:%s\n大小:%s \n时间:%s \n文件被修改时间:%s\nmd5:%s'%(data['server_filename'].encode('utf8'),str(round(float(data['size'])/1024/1024.0,2))+'MB',self.strTime(data['server_mtime']),self.strTime(data['local_mtime']),data['md5'].encode('utf8'))
        wx.MessageDialog(self.panel,mess,'文件详情',style=(wx.OK)).ShowModal()

    def getDownData(self,fdlist):
        postData={
                "fidlist":"[%s]"%fdlist,
                "type":"dlink",
                }
        url="http://pan.baidu.com/api/download?channel=chunlei&clienttype=0&web=1&bdstoken=%s"%self.bdstoken
        post=urllib.urlencode(postData)
        req=urllib2.Request(url,post,hds)
        print post
        print url
        print hds
        print urllib2.urlopen(req).read()



    def downFile(self): 
        dialog=wx.MessageDialog(self,'是否需要使用浏览器下载?','下载方式',style=wx.YES_NO)
        reqDialog=dialog.ShowModal()
        fileDict={}
        Id=self.spaceList.GetSelection()
        data=self.spaceItem[Id]
        fdlist=data["fs_id"]
        downData=self.getDownData(fdlist)
        req=urllib2.Request(data['dlink'],None,hds)
        page=urllib2.urlopen(req)
        url=page.geturl()
        url='http://' + '113.215.0.56' +'/cdn.baidupcs.com/' +url[url.find('file'):]
        if reqDialog == wx.ID_YES:
            print url
            webbrowser.open_new_tab(url)
        else:
            fileName=data['server_filename']
            fileDialog=wx.FileDialog(self,'保存到?','/data/',fileName,style=wx.SAVE|wx.OVERWRITE_PROMPT)
            if fileDialog.ShowModal() == wx.ID_OK:
                fileDict[fileName]=(data['md5'],fileDialog.GetPath())
                page=urllib2.urlopen(urllib2.Request(url,None,hds))
                self.showDownPro(fileDict[fileName],url,page)
    def showDownPro(self,fileItem,url,req):
        proDialog=wx.ProgressDialog('下载中...','正在下载',100,style=wx.PD_CAN_ABORT|wx.PD_AUTO_HIDE)
        fileMd5,fileSavePath=fileItem
        fileSize=req.info()['Content-Length']
        open(fileSavePath,'wb').close()
        threading.Thread(target=self.startDown,args=(fileSize,fileSavePath,url,req)).start()
        while True :
            if (not proDialog.Update(100.0*float(os.path.getsize(fileSavePath))/float(fileSize))[0]) or  float(os.path.getsize(fileSavePath)) >=float(fileSize) : #当取消进度条，或已下载文件的体积达到文件的大小，则结束进度条
                req.close()
                proDialog.Destroy()
                break
    def startDown(self,size,savePath,url,req):
        BUFSIZE=4096*2
        remoteFile=req
        fd=open(savePath,'wb')
        while True:
            try:
                data=remoteFile.read(BUFSIZE)#
            except:
                fd.close()
                os.remove(savePath)#当网络出错，或退出进度条时，就删除文件。
                break
            if not data or (not os.path.exists(savePath)):#如果读取完了，或那个文件不存在了，都要退出
                break
            fd.write(data)
        fd.close()
        print 'download finished'
        #webbrowser.open_new_tab(url)
    def strTime(self,t):
        return time.strftime("%Y-%m-%d %T",time.localtime(t))
    def getSpaceSize(self):
        url='http://pan.baidu.com/api/quota?channel=chunlei&clienttype=0&web=1&checkexpire=1&checkfree=1&bdstoken=%s'%self.bdstoken
        spaceSize=json.loads(urllib2.urlopen(url).read())
        totalSize='%.2fG'%(float(spaceSize['total'])/1024/1024/1024)
        usedSize='%.2fG'%(float(spaceSize['used'])/1024/1024/1024)
        self.spaceSize='%s/%s' %(usedSize,totalSize)
        WorkerThread(self,self.showSpaceSize).start()
    def getPageData(self):
        page=urllib2.urlopen('http://pan.baidu.com').read()
        re_bdstoken=re.compile(r'FileUtils\.bdstoken=\"(.+?)\"')
        re_cktoken=re.compile(r'FileUtils\.cktoken=\"(.+?)\";')
        re_uid=re.compile(ur'FileUtils\.sysUID=\"(.*?)\"')
        #re_space=re.compile(r'<span id=\"remainingSpace\">(.+?)</div>',re.S)
        self.uid=re_uid.findall(page)[0]
        self.bdstoken=re_bdstoken.findall(page)[0]
        self.cktoken=re_cktoken.findall(page)[0]
        #self.space=re_space.findall(page)[0]
        #self.space=re.sub(r'</?span>','',self.space)
        self.spaceUrl="http://pan.baidu.com/api/list?channel=chunlei&clienttype=0&web=1&num=100&page=1%&dir=%2Fdownloads%2F&order=time"+"&bdstoken=%s&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
        self.addUrl="http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=%s&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
        self.delUrl="http://pan.baidu.com/api/filemanager?channel=chunlei&clienttype=0&web=1&opera=delete&bdstoken=%s&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
        self.taskIdUrl="http://pan.baidu.com/rest/2.0/services/cloud_dl?bdstoken=%s&need_task_info=1&status=1&start=0&limit=10&method=list_task&app_id=250528&channel=chunlei&clienttype=0&web=1" %(str(self.bdstoken))
        self.myLock=threading.RLock()
class loginFrame(wx.Frame):
    def __init__(self,userName='',passWord='',isCheck=''):
        wx.Frame.__init__(self,None,-1,'请登录你的百度(作者:疯狂的小企鹅)',
                size=(350,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.Center()
        self.panel=wx.Panel(self,-1)
        userLabel=wx.StaticText(self.panel,-1,'账号: ',
                pos=(10,30),size=(50,-1))
        pwdLabel=wx.StaticText(self.panel,-1,'密码: ',
                pos=(10,60),size=(50,-1))
        labelPos=userLabel.GetSize()
        self.userText=wx.TextCtrl(self.panel,-1,userName,
                pos=(labelPos[0],30),size=(150,-1))
        self.pwdText=wx.TextCtrl(self.panel,-1,passWord,
                pos=(labelPos[0],60),size=(150,-1),style=wx.TE_PASSWORD)
        self.userText.SetFocus()
        self.checkText=wx.TextCtrl(self.panel,-1,"",pos=(240,60))
        self.checkLabel=wx.StaticText(self.panel,-1,"↑验证码↑",
                pos=(240,90))
        self.checkText.Show(False)
        self.checkLabel.Show(False)
        self.messLabel=wx.StaticText(self.panel,-1,"",
                pos=(30,150))
        self.button=wx.Button(self.panel,-1,"登录",
                pos=(30,120))
        self.checkBox=wx.CheckBox(self.panel,-1,'记住密码',
                pos=(labelPos[0],90))
        self.autoBox=wx.CheckBox(self.panel,-1,'自动登录',
                pos=(labelPos[0]+100,90))
        self.Bind(wx.EVT_CHECKBOX,self.OnCheck,self.autoBox)
        self.checkBox.SetValue(isCheck == '1')
        self.button.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.button)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.Show(True)
        self.bd=baidu()
        self.bd.initData()

    def OnClose(self,event):
        self.Destroy()
        sys.exit()

    def OnCheck(self,event):
        if self.autoBox.GetValue():
            wx.MessageBox("下次登录将自动进入离线下载器界面，不再需要登录~\n如果要取消自动登录，可以在设置菜单中选择\"关闭自动登录!\"","自动登录已开启")

    def OnClick(self,event):
        self.bd.t.join()
        if self.checkText.IsShown():self.setCode()
        user=self.userText.GetValue().encode('utf8')
        pwd=self.pwdText.GetValue().encode('utf8')
        loginPost['username']=user
        loginPost['password']=pwd
        if self.bd.sendPost():
            if self.checkBox.GetValue():
                writeDb(userName=user,passWord=pwd,isCheck='1')
            else:
                writeDb(userName='',passWord='',isCheck='')
            writeDb(isAuto=self.autoBox.GetValue())
            self.messLabel.SetLabel("登录成功")
            cj.save(cjUrl,ignore_discard=True, ignore_expires=True)
            self.Show(False)
            panFrame()
        else:
            self.showCode()
            self.messLabel.SetLabel("登录失败，请检查！")
            self.checkText.SetFocus()
    def showCode(self):
        if self.bd.getCode():
            img=wx.Image(TempCodeImg,wx.BITMAP_TYPE_ANY)
            self.checkText.Show(True)
            self.checkLabel.Show(True)
            self.checkCodeImg=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(img),pos=(240,20))
            os.remove(TempCodeImg)
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
            urllib.urlretrieve(imgUrl,TempCodeImg)
            return True
        except Exception:
            pass
            return False
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
        
if __name__=='__main__':
    cj=cookielib.MozillaCookieJar()
    app=wx.App()
    def loginBd():
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        mutex=threading.Lock()
        lFrame=loginFrame(**readDb('userName','passWord','isCheck'))

    def autoLogin():
        try:
            cookies=cookielib.MozillaCookieJar(cjUrl)
            cookies.load(ignore_discard=True,ignore_expires=True)
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
            urllib2.install_opener(opener)
            panFrame()
        except Exception,e:
            loginBd()
            return False
    if readDb('isAuto')['isAuto']:
        autoLogin()
    else:
        loginBd()
    app.MainLoop()
    
