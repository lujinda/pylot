import wx
if __name__=='__main__':
    app=wx.App()
    dialog=wx.DirDialog(None,"Choose a directory:",
            style=wx.DD_DEFAULT_STYLE)
    if dialog.ShowModal()==wx.ID_OK:
        print dialog.GetPath()
    dialog.Destroy()
