import wx
class SpinnerFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,"spinner example",size=(200,100))
		panel=wx.Panel(self,-1)
		sc=wx.SpinCtrl(panel,-1,"",(30,20),(80,-1),max=100,min=1,initial=5)
		s=wx.SpinButton(panel,-1)
		
if __name__=='__main__':
	app=wx.App()
	frame=SpinnerFrame()
	frame.Show()
	app.MainLoop()

