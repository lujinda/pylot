#coding:utf8
import wx
import sys
import urllib2
import urllib
import os
import threading

class WorkerThread(threading.Thread):
    def __init__(self,fun,*args):
        threading.Thread.__init__(self)
        self.fun=fun
       # self.timeToQuit=threading.Event()
       # self.timeToQuit.clear()
        self.args=args
    def run(self):
        wx.CallAfter(self.fun,*self.args)

class downFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'请开始下载!',size=(300,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.panel=wx.Panel(self,-1)
        downBut=wx.Button(self.panel,-1,'下载',size=self.GetSizeTuple())
        self.Bind(wx.EVT_BUTTON,self.OnDown,downBut)
        self.Center()
        self.Show()
    def OnDown(self,event):
        try:
            fileUrl=sys.argv[1]
        except Exception,e:
            print '请在命令后加一个url地址好吗？亲～'
            self.Destroy()
            sys.exit()
        self.startDown(fileUrl)
        
    def startDown(self,fileUrl):
        fileDialog=wx.FileDialog(self,message='请选择保存位置:',defaultDir='/home/ljd/Desktop/',defaultFile='win8.1.iso',style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if fileDialog.ShowModal()==wx.ID_OK:
            fileName=fileDialog.GetPath()
            req=urllib2.urlopen(fileUrl)
            fileSize=req.info()['Content-Length']
            threading.Thread(target=self.downFile,args=(fileName,req)).start()
            WorkerThread(self.showDown,fileName,fileSize,req).start()
            #wx.CallAfter(self.showDown,fileName,fileSize,req)
    def showDown(self,fileName,fileSize,req):
        proDialog=wx.ProgressDialog('下载中...','正在下载:',100,style=wx.PD_CAN_ABORT|wx.PD_AUTO_HIDE)
        while True:
            if  (not  os.path.lexists(fileName) )or (not proDialog.Update(100.0*float(os.path.getsize(fileName))/float(fileSize))[0] ) or float(os.path.getsize(fileName)) >=float(fileSize):
                proDialog.Destroy()
                req.close()
                break
            
    def downFile(self,fileName,fileReq):
        BUFSIZE=4096*2
        saveFile=open(fileName,'wb')
        while True:
            try:
                data=fileReq.read(BUFSIZE)
            except:
                saveFile.close()
                os.remove(fileName)
                WorkerThread(self.showMess,'任务被取消或网络出问题，已停止下载','出错了～',wx.OK).start()
                break
            if not data:break
            saveFile.write(data)
        saveFile.close()
    def showMess(self,*args):
        wx.MessageBox(args[0],args[1],style=args[2])
def authUser():
    BUFSIZE=4096*2
    pmg=urllib2.HTTPPasswordMgrWithDefaultRealm()
    pmg.add_password(None,'http://172.16.0.5:8080','www-data','1')
    handler=urllib2.HTTPBasicAuthHandler(pmg)
    opener=urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    """
req=urllib2.urlopen(fileUrl)
fileSize=req.info()['Content-Length']

while True:
    """

if __name__=='__main__':
    authUser()
    app=wx.App()
    downFrame()
    app.MainLoop()
