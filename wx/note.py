#coding:utf8
import wx,config
class LoginFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,title="请登录",size=(200,150),pos=(100,100),style=wx.CAPTION|wx.CLOSE_BOX)
		panel=wx.Panel(self,-1)
		sizer=wx.FlexGridSizer(3,2,6,6)
		hbox=wx.BoxSizer(wx.HORIZONTAL)
		self.userLabel=wx.StaticText(panel,-1,"账号:")
		self.pwdLabel=wx.StaticText(panel,-1,"密码:")
		self.userText=wx.TextCtrl(panel,-1,"")
		self.pwdText=wx.TextCtrl(panel,-1,"",style=wx.TE_PASSWORD)
		button=wx.Button(panel,-1,"登录",size=(50,-1))
		button.SetDefault()
		sizer.AddMany([self.userLabel,self.userText,self.pwdLabel,self.pwdText,button])
		hbox.Add(sizer,proportion=1,flag=wx.ALL|wx.EXPAND,border=26)
		self.Bind(wx.EVT_BUTTON,self.OnClick,button)
		panel.SetSizer(hbox)
	def OnClick(self,event):
		t=config.Db()
		if not t.checkPwd(self.userText.GetValue(),self.pwdText.GetValue()):
			dlg=wx.MessageDialog(self,"请检查您的用户名和密码","登录失败",style=wx.OK)
		else:
			dlg=wx.MessageDialog(self,"登录成功","登录成功",style=wx.OK)
		dlg.ShowModal()
		self.pwdText.Clear()
		self.pwdText.SetFocus()
		

if __name__=='__main__':
	App=wx.App()
	loginFrame=LoginFrame()
	loginFrame.Show()
	App.MainLoop()
