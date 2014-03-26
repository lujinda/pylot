import wx
if __name__=='__main__':
    app=wx.App()
    dialog=wx.FontDialog(None,wx.FontData())
    if dialog.ShowModal()==wx.ID_OK:
        data=dialog.GetFontData()
        font=data.GetChosenFont()
        print type(font)
        print type(wx.Font())
