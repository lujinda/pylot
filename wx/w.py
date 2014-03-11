#!/bin/env python
import thread
import threading,wx
import time
import urllib,urllib2
hds={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 '}
class WorkerThread(threading.Thread):
    def __init__(self,fuc,window):
        threading.Thread.__init__(self)
        self.window=window
        self.timeToQuit=threading.Event()
        self.timeToQuit.clear()
        self.fuc=fuc
    
    def run(self):
        #time.sleep(1)
        #self.timeToQuit.wait(1)
        wx.CallAfter(self.fuc)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title="Multi-thread get page")
        self.Center()
        self.threads=[]
        panel=wx.Panel(self)
        getBtn=wx.Button(panel,-1,"get a page")
        self.page=wx.TextCtrl(panel,-1,"",style=wx.TE_CENTER|wx.TE_MULTILINE)
        
        inner=wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(getBtn,0,wx.RIGHT,15)
        main=wx.BoxSizer(wx.VERTICAL)
        main.Add(inner,0,wx.ALL,5)
        main.Add(self.page,1,wx.EXPAND|wx.ALL,5)
        panel.SetSizer(main)
        self.Bind(wx.EVT_BUTTON,self.OnClick,getBtn)

    def OnClick(self,event):
    #   self.page.Clear()
        threading.Thread(target=self.getPage).start()
        #thread.start_new_thread(self.gp,())
    def SetText(self):
        self.page.SetValue(unicode(self.text,'gbk').encode('utf8'))
        #time.sleep(2)
        #self.page=""
        #threading.Thread(target=self.getPage).start()

    def getPage(self):
        url='http://www.qq.com'
        req=urllib2.Request(url,None,hds)
        page=urllib2.urlopen(req).read()
        self.text=page
        WorkerThread(self.SetText,self).start()
        #print unicode(page,'gbk').encode('utf8')
        #self.page.SetValue(unicode(page,'gbk').encode('utf8'))

app=wx.App()
frame=MyFrame()
frame.Show()
app.MainLoop()
