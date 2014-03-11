#!/usr/bin/env python
#coding:utf8
"""
部分变量名说明：
	self.fileName 在程序中表示正在操作的文件，默认为空，表示未打开任何文件
	self.fileType 在没有打开过文件时，默认为空，表示可以另存为任何一种格式，当打开一个文件时，文件的后缀给这个变量，这时保存时就有过滤了
	self.ITEM主要是用于记录菜单项的，在创建加速器的时候要用到
	self.Dencoding记录了被打开文件的编码，如果不是utf8，则把它转成utf8
	截止2014-1-19，这只有最简单的功能，不过我挺喜欢简单的东西的，在日常使用过程中，如果发现有不习惯的地方，还会一直往里面加功能的。本人新手小白，努力把这个打造成自己习惯的简单记事本
	self.IsCli 主要是用来判断是否在命令行下打开文件的。判断依据就是filename，如果有的话，就说明是
	self.downKc主要是用来控制加大字体，减少字体快捷键的
	self.fontSize=defontSize 记录着文字大小
	ctrl + ] 和ctrl + [ 分别是增大／减小字体的快捷键，ctrl + =是还原成默认的的
	目前布局还是个蛋疼的地方
	恢复当用命令行打开一个空文件时，无法正常保存（编码问题）
	恢复无法打开一个当前不存在的文件
	以上截止2014-1-20
"""
import wx
import os
import time
import chardet
import sys
class MyFrame(wx.Frame):
	def __init__(self,parent,pos=(150,150),filename=""):
		wx.Frame.__init__(self,parent,-1,title="疯狂的小企鹅的记事本",pos=pos,size=(700,650))#create a frame
		panel=wx.Panel(self,-1)
		fsize=self.GetSize()
		self.initData(filename)#initialization data
		self.createMenuBar()
		self.Text=wx.TextCtrl(panel,-1,"",size=(200,300),style=wx.TE_MULTILINE|wx.TE_RICH)
		self.Text.SetFocus()
		self.createStatusBar()
		self.Bind(wx.EVT_SIZE,self.OnResize)
		self.Bind(wx.EVT_IDLE,self.OnIdle)
		self.Bind(wx.EVT_CLOSE,self.OnClose)

		ctrlO=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('O'),self.ITEM[0].GetId())])
		ctrlS=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('S'),self.ITEM[1].GetId())])
		ctrlN=wx.AcceleratorTable([(wx.ACCEL_CTRL,ord('N'),self.ITEM[3].GetId())])
		self.SetAcceleratorTable(ctrlO)
		self.SetAcceleratorTable(ctrlS)
		self.SetAcceleratorTable(ctrlN)
		if self.IsCli:self.OpenFile()
			
	def initData(self,filename):
		self.iPos=0
		self.xyPos=0
		defontSize=12#default font size is 12
		self.fontSize=defontSize
		self.font=wx.Font(defontSize,wx.DEFAULT,style=wx.NORMAL,weight=wx.NORMAL)
		self.Dencoding='utf-8'
		self.ITEM=[]
		self.fileName=filename
		self.downKc={
			93:lambda :self.fontSize+5,  #93 == ]
			91:lambda :self.fontSize-5,#91==[
			61:lambda :defontSize,#61== =

		}
		if self.fileName:
			self.IsCli=True
		else:
			self.IsCli=False
		self.fileType="*"#some defaults 
	def createStatusBar(self):
		self.statusBar=self.CreateStatusBar()
		self.statusBar.SetFieldsCount(4)
		self.statusBar.SetStatusWidths([-2,-2,-3,-3])
		self.statusBar.SetStatusText('疯狂的小企鹅 http://linux.zj.cn',3)
		self.Text.Bind(wx.EVT_TEXT,self.OnText,self.Text)
		self.Text.Bind(wx.EVT_KEY_UP,self.OnDown,self.Text)
		self.Text.Bind(wx.EVT_LEFT_UP,self.OnText,self.Text)
	def OnText(self,event):
			self.iPos=self.Text.GetInsertionPoint()
			self.xyPos=self.Text.PositionToXY(self.iPos)
			self.statusBar.SetStatusText("x: %s y: %s Lines: %d"%(self.xyPos[0],self.xyPos[1],self.Text.GetNumberOfLines()),0) #display x,y and lines
			event.Skip()
	
	def menuData(self):
		return (("&File",
					("&Open\tCtrl-O","open a file",self.OnOpen),
					("&Save\tCtrl-S","save file",self.OnSave),
					("&Save as","",self.OnSaveAs),
					("&Save as(to utf-8)","",self.OnSaveAsU),
					("&Save as(to gbk)","",self.OnSaveAsG),
					("&New\tCtrl-N","",self.OnNew),
					("","",""),
					("&Quit","close me",self.OnCloseWindow)),
				("&Help",
				  ("&About","about me",self.OnAbout))
				)
	def createMenuBar(self):
		menuBar=wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel=eachMenuData[0]
			menuItems=eachMenuData[1:]
			menuBar.Append(self.createMenu(menuItems),menuLabel)
		self.SetMenuBar(menuBar)
	
	def createMenu(self,menuData):
		menu=wx.Menu()
		for eachLabel,eachStatus,eachHandler in menuData:
			if not eachLabel:
				menu.AppendSeparator()#create -----------in menu
				continue
			menuItem=menu.Append(wx.NewId(),eachLabel,eachStatus)
			self.ITEM.append(menuItem)
			self.Bind(wx.EVT_MENU,eachHandler,menuItem)
		return menu
	def ReFont(self):
		self.Text.SetStyle(0,-1,wx.TextAttr(font=self.font))#set font style,but I don't know ,why I set SetDefaultStyle not working

	def OnIdle(self,event):
		self.statusBar.SetStatusText(time.strftime("%Y-%m-%d %H:%M",time.localtime()),1)
		self.ReFont()
#show time on statusbar[0]
	def OnClose(self,event):
		dlg=wx.MessageDialog(self,"是否保存您的文档","请认真做出判断",style=wx.YES_NO|wx.CANCEL|wx.YES_DEFAULT|wx.ICON_QUESTION)
		dlgQ=dlg.ShowModal()
		if dlgQ==wx.ID_YES:
			self.OnSave(event)
			self.Destroy()
		if dlgQ==wx.ID_NO:self.Destroy()
		if dlgQ==wx.ID_CANCEL:pass
	def OnDown(self,event):
		kc=event.GetKeyCode()
		if 314<=kc<=317:self.OnText(event)
		if self.fontSize<5:self.fontSize=5
		if event.ControlDown():
			try:
				self.fontSize=self.downKc[kc]()
				self.font=wx.Font(self.fontSize,wx.DEFAULT,style=wx.NORMAL,weight=wx.NORMAL)
			except:
				pass
		event.Skip()
	def OnResize(self,event):
		self.Text.Size=(self.GetSize()[0],self.GetSize()[1]-22)
		event.Skip()
	def SaveFile(self,filename):
		try:
			fd=open(filename,"w")
			fd.write(self.Text.GetValue().encode(self.Dencoding))
			fd.close()
			self.fileName=filename
			self.changeF()
		except:
			pass
			
	def OnSaveAs(self,event):
		wSave=wx.FileDialog(self,message="save to ...",defaultDir=os.getcwd(),style=wx.SAVE|wx.OVERWRITE_PROMPT,wildcard=self.fileType)
		if wSave.ShowModal() == wx.ID_OK:
			filename=wSave.GetPath()
			self.SaveFile(filename)

	def OnSave(self,event):
		if not self.fileName:self.OnSaveAs(event)
		self.SaveFile(self.fileName)
	def OpenFile(self):
		try:
			fd=open(self.fileName,'rb')
			content=fd.read()
			self.Dencoding=chardet.detect(content)['encoding']
			if self.Dencoding=='ascii' or self.Dencoding == None:self.Dencoding='utf-8'
			content=unicode(content,self.Dencoding).encode('utf-8')#change encoding
			self.Text.write(content)
			self.Text.SetInsertionPoint(0)
			self.Text.ShowPosition(0)
			fd.close()
		except Exception,e:
			if e.errno!=2:self.fileName=""
#print e
		self.changeF()
			
	def OnOpen(self,event):
		wOpen=wx.FileDialog(self,message="select a file",defaultDir=os.getcwd(),style=wx.OPEN)
		if wOpen.ShowModal() == wx.ID_OK:
			self.Text.Clear()
			self.fileName=wOpen.GetPath()#get filename
			self.fileType="*.%s" %(self.fileName.split('.')[-1])#get filetype
			self.OpenFile()
	def changeF(self):
			self.SetTitle(self.fileName)
			self.statusBar.SetStatusText(self.fileName,2)

	def OnCloseWindow(self,event):
		self.OnClose(event)
	def OnNew(self,event):
		newPos=tuple([x+50 for x in self.GetPositionTuple()])
		frame=MyFrame(None,pos=newPos)
		frame.Show()
	def OnAbout(self,event):
		import webbrowser
		webbrowser.open_new_tab('http://linux.zj.cn')
	def OnSaveAsG(self,event):
		self.Dencoding='gbk'
		self.OnSaveAs(event)
	def OnSaveAsU(self,event):
		self.Dencoding='utf-8'
		self.OnSaveAs(event)

if __name__=='__main__':
	app=wx.PySimpleApp()
	try:
		open(sys.argv[1],'r').close()
		cliFilename=sys.argv[1]
	except Exception,e:
		try:
			if e.errno==2:
				cliFilename=sys.argv[1]
			else:
				cliFilename=""
		except:
			cliFilename=""
	frame=MyFrame(None,filename=cliFilename)
	frame.Show()
	app.MainLoop()
