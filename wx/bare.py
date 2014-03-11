import wx
class App(wx.App):
	def OnInit(self):
		frame=wx.Frame(parent=None)
		frame.Show(True)
		return True
app=App()
app.MainLoop()
