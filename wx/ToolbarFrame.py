import wx
class ToolbarFrame(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,'ToolBars',size=(300,200))
		panel=wx.Panel(self)
		panel.SetBackgroundColour('#ffffffff')
		statusBar=self.CreateStatusBar()
		toolbar=self.CreateToolBar()
#		toolbar.AddSimpleTool(wx.NewId(),images.getNewBitmap(),"New","Long help")
		toolbar.Realize()
		menuBar=wx.MenuBar()
		menu1=wx.Menu()
		item=menu1.Append(-1,"def")
		menuBar.Append(menu1,"abc")
		self.SetMenuBar(menuBar)
if __name__=='__main__':
	app=wx.PySimpleApp()
	frame=ToolbarFrame(None,-1)
	frame.Show()
	app.MainLoop()
