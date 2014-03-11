#!/usr/bin/env python
#coding:utf8
import sys,base64,re,wx,chardet,urllib2,threading
hds={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
        }
class WorkerThread(threading.Thread):
    def __init__(self,window,fun,*args):
        threading.Thread.__init__(self)
        self.window=window
        self.fun=fun
        self.args=args[0]
    def run(self):
        wx.CallAfter(self.fun,self.args)


def getThunder(url):
    url="AA%sZZ" %url
    return "thunder://" + base64.encodestring(url).replace('\n','') #encodestring之后中，会有个换行符，我们要删掉这经
def getQqdl(url):
    return "qqdl://" + base64.encodestring(url).replace('\n','')
def getFlashget(url):
    url="[FLASHGET]" + url +"[FLASHGET]"
    return "flashget://" + base64.encodestring(url).replace('\n','')+'&1926'
    
def getUrl(url):
    if url.lower().startswith('thunder://'):
        url=base64.decodestring(url[10:])
        url=url[2:-2]
    elif url.lower().startswith('flashget://'):
        url=base64.decodestring(url[11:url.find('&')])
        url=url[10:-10]
    elif url.lower().startswith('qqdl://'):
        url=base64.decodestring(url[7:])
    elif re.match(r'^(https?|ftp)://',url.lower()):#match http(s)或ftp开头的地址,表示是真实地址
        url=url
    else:
        url=""
    return url
class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'疯狂的地址转换(q8886888@qq.com)',size=(600,300),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.panel=wx.Panel(self,-1)
        self.inText=wx.TextCtrl(self.panel,-1,"",pos=(100,10),size=(450,-1))
        self.inText.SetFocus()
        self.createLabel()
        self.createText()
        button=wx.Button(self.panel,-1,'转换',pos=(300,250),size=(-1,-1))
        self.detailBtn=wx.Button(self.panel,-1,'查看headers',pos=(200,250),size=(-1,-1))
        self.detailBtn.Enable(False)
        button.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnClick,button)
        self.Bind(wx.EVT_BUTTON,self.OnDetail,self.detailBtn)
        self.Center()
        wx.TheClipboard.Flush()
        self.Show()
    def OnDetail(self,event):
        self.detailBtn.Enable(False)
        threading.Thread(target=self.showHeaders).start()
    def showHeaders(self):
        req=urllib2.Request(self.url,None,hds)
        try:
            result=urllib2.urlopen(req,timeout=5)
            WorkerThread(self,self.showMess,result.headers).start()
        except Exception,e:
            if 'code' not in dir(e):e.code='---'
            WorkerThread(self,self.showMess_error,str(e.code)).start()
            

    def showMess_error(self,code):
        wx.MessageDialog(self.panel,'url:%s\nerror_code:%s\n'%(self.url,code),'Error',style=wx.OK).ShowModal()
        
        self.detailBtn.Enable(True)

    def showMess(self,headers):
        try:
            fileSize=float(headers['Content-Length'])
            if fileSize>1048576:
                fileSize="文件大小:%0.2f MB" % (fileSize/1024/1024.0)
            else:
                fileSize="文件大小:%0.2f KB" % (fileSize/1024.0)
        except:
            fileSize=""
        wx.MessageDialog(self.panel,fileSize +'\n' +str(headers),'headers',style=wx.OK).ShowModal()
        self.detailBtn.Enable(True)
    def OnDclick(self,event):
        data=wx.TextDataObject()
        url=event.GetEventObject().GetValue()
        data.SetText(url)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()#如果不Close，则接下来就无法复制
            self.SetTitle("地址已复制:" + url.encode('utf8'))#ascii to utf8
    def OnClick(self,event):
        self.url=getUrl(self.inText.GetValue())
        if self.url:
            self.textItem[0].SetValue(self.url)
            self.textItem[1].SetValue(getQqdl(self.url))
            self.textItem[2].SetValue(getFlashget(self.url))
            self.textItem[3].SetValue(getThunder(self.url))
            self.detailBtn.Enable(True)
            self.inText.Clear()
        else:
            wx.MessageBox('输入地址有误，请检查','出错喽～～',style=wx.OK)
            self.url=self.textItem[0].GetValue().encode('utf8')
            self.inText.Clear()
    def createLabel(self):
        for data in self.labelData():
            wx.StaticText(self.panel,data[0],data[1],data[2])
    def createText(self):
        self.textItem=[]
        for data in self.textData():
            item=wx.TextCtrl(self.panel,-1,"",pos=data[0],size=(450,-1),style=data[1])
            self.textItem.append(item)
            item.Bind(wx.EVT_LEFT_DCLICK,self.OnDclick)
            
    def labelData(self):
        return (
                (-1,"请输入地址:",(10,10)),
                (-1,"原始地址:",(10,60)),
                (-1,"旋风地址:",(10,110)),
                (-1,"快车地址:",(10,160)),
                (-1,"迅雷地址:",(10,210)),
                )
    def textData(self):
        return (
                ((80,60),wx.TE_READONLY),
                ((80,110),wx.TE_READONLY),
                ((80,160),wx.TE_READONLY),
                ((80,210),wx.TE_READONLY),
                )

if __name__=='__main__':
    app=wx.App()
    frame=myFrame()
    app.MainLoop()
