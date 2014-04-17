import wx

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Test!",size=(200,100))
        self.Center()
        self.panel=wx.Panel(self)
        wx.TextCtrl(self.panel,-1,"",pos=(10,10))
        wx.TextCtrl(self.panel,-1,"",pos=(100,10))
        wx.Button(self.panel,-1,"Button",pos=(20,50))

if __name__=="__main__":
    app=wx.App()
    myFrame().Show()
    app.MainLoop()
