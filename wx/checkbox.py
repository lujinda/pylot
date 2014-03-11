import wx
class CheckBoxFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,'Checkbox Example',size=(150,200))
		self.panel=wx.Panel(self,-1)
	
		self.CreateBoxData()
	def CreateBoxData(self):
		for data in self.CheckBoxData():
			cb=wx.CheckBox(self.panel,-1,data[0],data[1],data[2])
			self.Bind(wx.EVT_CHECKBOX,self.Click,cb)
	def Click(self,event):
		print event.GetId()
	def CheckBoxData(self):
		return (("Aplpha",(35,40),(150,20)),
				("Bete",(35,60),(150,20)),
				("Gamma",(35,80),(150,20))
				)

if __name__=='__main__':
	app=wx.App()
	frame=CheckBoxFrame()
	frame.Show()
	app.MainLoop()
