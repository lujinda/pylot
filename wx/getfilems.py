#!/usr/bin/env python
#coding:utf8
import hashlib
import wx
import os
import sys
from os.path import getsize
import time

if __name__=='__main__':
    def showMess(fileName,userTime,fileSize,md5=None,sha1=None):
        wx.MessageBox(u'文件名:%s\n文件大小:%s\nmd5:%s\nsha1:%s'%(fileName,fileSize,md5,sha1),u'耗时:%f 秒' %(userTime),style=wx.OK)
        fd.close()
    BUFSIZE=4096*2
    app=wx.App()
    fileDialog=wx.FileDialog(None,"Choose a file",os.getcwd(),style=wx.FD_OPEN)
    if fileDialog.ShowModal() == wx.ID_OK:
        fileName=fileDialog.GetPath()
        fileSize=getsize(fileName)
        old=time.time()
        proDialog=wx.ProgressDialog("正在计算中...",'正在计算中...',100,style=wx.PD_CAN_ABORT|wx.PD_AUTO_HIDE)
        proValue=0
        fd=open(fileName,'rb')
        md5obj=hashlib.md5()
        sha1obj=hashlib.sha1()
        fileDialog.Destroy()
        while True:
            data=fd.read(BUFSIZE)
            proValue+=BUFSIZE
            if not data:
                break
            if not proDialog.Update(100.0*proValue/fileSize)[0]:
                showMess(fileName=fileName,userTime=time.time()-old,fileSize=fileSize)
                proDialog.Destroy()
                sys.exit()
            sha1obj.update(data)
            md5obj.update(data)
        showMess(md5=md5obj.hexdigest(),sha1=sha1obj.hexdigest(),fileName=fileName,userTime=time.time()-old,fileSize=fileSize)
        proDialog.Destroy()
