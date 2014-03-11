#coding:utf8
import wx

class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"wx.ListCtrl in wx.LC_REPORT mod",size=(600,400))
        self.List=wx.ListCtrl(self,-1,style=wx.LC_REPORT)
        self.List.InsertColumn(0,'文件名')
        self.List.InsertColumn(1,'文件大小')
        self.List.InsertStringItem(0,'abc')
        self.List.InsertStringItem(1,'abc')
        self.List.InsertStringItem(2,'def')
        self.List.SetStringItem(0,1,'30')
        print self.List.GetItemText(2)

app=wx.App()
frame=DemoFrame()
frame.Show()
app.MainLoop()
