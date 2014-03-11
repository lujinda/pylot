#!/usr/bin/env python
#coding:utf8
import wx,sys,os,time,subprocess
from PIL import Image

def spiltImg(imgFile):
    im=Image.open(imgFile)
    im.seek(0)
    tIm=Image.new(im.mode,im.size)
    p=im.getpalette()
    c=1
    try:
        while True:
            tIm=im
            tIm.putpalette(p)
            tIm.save('temp_gifImg/%s_%d.gif'%(imgFile[:-4],c),'gif',transparency=0,quality=100)
            im.seek(im.tell()+1)
            c+=1
    except EOFError:
        pass

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"疯狂GIF提取(q8886888@qq.com))",size=(200,162))
        self.panel=wx.Panel(self,-1)
        self.Center()
        self.openButton=wx.Button(self.panel,-1,"选择图片",size=(200,80),pos=(0,0))
        self.openButton.SetDefault()
        self.showButton=wx.Button(self.panel,-1,"打开目录",size=(200,80),pos=(0,80))
        self.showButton.Enable(False)
        self.Bind(wx.EVT_BUTTON,self.OnOpen,self.openButton)
        self.Bind(wx.EVT_BUTTON,self.OnShow,self.showButton)
        self.Show()
    def OnOpen(self,event):
        wOpen=wx.FileDialog(self,message="Choose a gif image:",defaultDir=os.getcwd(),style=wx.OPEN,wildcard='*.gif')
        if wOpen.ShowModal() == wx.ID_OK:
            fileName=wOpen.GetPath()
            self.dirName=os.path.dirname(fileName)
            fileName=wOpen.GetFilename()
            os.chdir(self.dirName)
            try:
                os.mkdir('temp_gifImg')
            except:
                pass
            spiltImg(fileName)
            self.showButton.Enable(True)
            
            
            
    def OnShow(self,event):
        subprocess.Popen(['xdg-open',self.dirName+'/temp_gifImg'])

if __name__=='__main__':
    app=wx.App()
    frame=myFrame()
    app.MainLoop()
