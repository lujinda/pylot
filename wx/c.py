#coding:utf8
import thread,threading,wx,socket,sys,random,re


class cFrame(wx.Frame):
    def __init__(self,client,UserName):
        wx.Frame.__init__(self,None,-1,'聊天室信息',size=(700,500))
        self.Center()
        self.sock=client
        self.userName=UserName
        self.ShowElemts()
        self.showClient()
        self.Show()
        
    def ShowElemts(self):
        x=20
        self.panel=wx.Panel(self,-1)
        self.clientList=wx.ListBox(self.panel,-1,pos=(400,x),size=(280,300))
        self.chatBox=wx.TextCtrl(self.panel,-1,style=wx.TE_MULTILINE|wx.TE_READONLY,pos=(10,x),size=(380,300))
        self.messBox=wx.TextCtrl(self.panel,-1,style=wx.TE_MULTILINE,pos=(10,340),size=(380,100))
        self.sendBut=wx.Button(self.panel,-1,'发送',pos=(10,460),size=(380,30))

        self.createMenu()
    def showClient(self):
        self.sock.send('list_client')
        self.clientList.Clear()
        clientList=self.sock.recv(2048).split('\n')
        for client in clientList:
            if client:self.clientList.Append(client)
        
    def menuData(self):
        return (
                ('设置',
                    ('修改网名','修改聊天室中的名字',self.entryUser),
                    ('退出聊天室','退出聊天室，并关闭程序',self.exitChat),
                ),
                )
    def createMenu(self):
        menuBar=wx.MenuBar()
        for eachData in self.menuData():
            label=eachData[0]
            menuItems=eachData[1:]
            menuBar.Append(self.createMenuItem(menuItems),label)
        self.SetMenuBar(menuBar)
    
    def createMenuItem(self,eachData):
        menu=wx.Menu()
        for label,status,handler in eachData:
            item=menu.Append(wx.NewId(),label,status)
            self.Bind(wx.EVT_MENU,handler,item)
        return menu
        
    def entryUser(self,event):
        dialog=wx.GetTextFromUser('请输入网名(最长15位):','修改网名',self.userName).strip()
        while len(dialog)>=15:
            dialog=wx.GetTextFromUser('请输入网名(最长15位):','修改网名',self.userName).strip()
        if dialog:
            self.userName=dialog
            self.sock.sendall('change_name')
            self.changeUser()
            self.showClient()
        
    def changeUser(self):
        wx.Sleep(1)
        self.sock.sendall(self.userName)
    def exitChat(self,event):
        self.Destroy()
#class loginFame(wx.):



if __name__=='__main__':
    app=wx.App()
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverIp=wx.GetTextFromUser(message='请输入服务器地址:',caption='请输入',default_value='172.16.0.5')
        sock.connect((serverIp,4567))
        UserName='UnKnow'+str(random.randrange(1000,9999))
        sock.send(UserName)
    except Exception,e:
        dialog=wx.MessageDialog(None,str(e),'出错了哦')
        dialog.ShowModal()
        sys.exit()
    clientFrame=cFrame(sock,UserName)       
    app.MainLoop()


