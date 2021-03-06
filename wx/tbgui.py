#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部分变量，函数说明：
post是经postData,urlencode后的
函数名:
    getTime,setButton获取当前时间，用作最后更新时间,并把它作为刷新按钮的label
    OnDataClick[0-3]是那一行的四颗刷新按钮
    showJf,showBalance,showPaiInfo,showRefunding,showExInfo分别显示积分，余额，待发货信息，退款中的信息，已发货信息和物流信息。有些要显示到listbox
    getName,getDealTime,getExUrl分别用来获取宝贝名字，成交时间和金额，物流信息的url
变量名:
    self.pageData保存的是当前前面的内容，要被后面匹配的。只有在getName中对它进行赋值
    exText表示最下面最大的那个物流文本框。
    self.payTime[0]里面存的是待收货的每件宝贝的成交时间和金额[1]存的是未发货的，[2]的是退款中的
    self.xxxItem存的是对应控件
    
"""
import urllib,urllib2,chardet,cookielib,re,json,wx,sys,time,thread,tempfile,os
import socket
hds={
        'Accept':'exxt/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
}
 
url='https://login.taobao.com/member/login.jhtml'#登录地址,login address
notUrl='http://trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1&auctionStatus=SEND&tradeRemindFrom=SEND'
searchUrl='http://trade.taobao.com/trade/itemlist/list_bought_items.htm?search'
balanceUrl='http://i.taobao.com/json/getFinanceBalance.htm'
jfUrl='http://i.taobao.com/json/privilege.htm'

class imgFrame(wx.MiniFrame):
    def __init__(self,window,pos,url):
        #pre=wx.PreFrame()
        #pre.SetExtraStyle(wx.F)
        #pre.Create(window,-1,title='宝贝照片',pos=pos,style=wx.SIMPLE_BORDER)
        wx.MiniFrame.__init__(self,window,-1,'宝贝照片',pos=pos,style=wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT)
        #pre.Create(window,-1,title='宝贝照片',pos=pos,style=wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW)
        #self.PostCreate(pre)
        imgFile=tempfile.mkstemp()[1]+'.jpg'
        self.panel=wx.Panel(self,-1)
        fd=open(imgFile,'wb')
        try:
            fd.write(urllib2.urlopen(url,timeout=2).read())
            fd.close()
            img=wx.Image(imgFile,wx.BITMAP_TYPE_ANY)
            self.SetSize(img.GetSize())
            bitImg=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(img))
            bitImg.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
            os.remove(imgFile)
        except Exception,e:
            self.SetTitle('获取宝贝照片失败')
            self.panel.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
            fd.close()
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)
        self.Bind(wx.EVT_MOTION,self.OnMouseMove)
        self.Bind(wx.EVT_CLOSE,self.OnClose)

    def OnClose(self,event):
        self.Destroy()

    def OnLeftDown(self,event):
        print 'Down'
        self.CaptureMouse()
        pos=self.ClientToScreen(event.GetPosition())
        fpos=self.GetPosition()
        self.dataPos=wx.Point(pos.x-fpos.x,pos.y-fpos.y)

    def OnMouseMove(self,event):
        if event.Dragging() and event.LeftIsDown():
            pos=self.ClientToScreen(event.GetPosition())
            newPos=(pos.x-self.dataPos.x,pos.y-self.dataPos.y)
            self.Move(newPos)

    def OnLeftUp(self,event):
        if self.HasCapture():
            self.ReleaseMouse()

class taobaoFrame(wx.Frame):
    def __init__(self,user,pwd):
        wx.Frame.__init__(self,None,-1,"淘宝信息(作者:q8886888@qq.com)",size=(700,600),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.panel=wx.Panel(self,-1)
        exButton=wx.Button(self.panel,-1,"刷新物流",pos=(100,265),size=(-1,28))
        self.Bind(wx.EVT_BUTTON,self.OnExClick,exButton)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.exText=wx.TextCtrl(self.panel,-1,"",pos=(-1,300),size=(700,300),style=wx.ALIGN_LEFT|wx.TE_MULTILINE|wx.TE_READONLY)
        self.tb=taobao()
        self.payTime=["","",""]
        self.tb.postData['TPL_username']=user
        self.tb.postData['TPL_password']=pwd
        self.createLabel()
        self.createList()
        self.createDataButton()
        self.Center()
        self.Show(True)
        self.showExInfo()
        self.showBalance()
        self.showJf()
        self.showPaiInfo() #显示已经拍下，但未发货的
        self.showRefunding()#显示正在退款中的
        self.timer=wx.Timer(self,-1)
        self.Bind(wx.EVT_TIMER,self.OnTime,self.timer)
        self.timer.Start(1000*60*15)
    def OnTime(self,event):
        thread.start_new_thread(self.updataCj,())
    def updataCj(self):
        try:
            t=urllib2.urlopen('http://trade.taobao.com/trade/itemlist/list_bought_items.htm')
        except:
            pass
        t.close()
        thread.exit_thread()
    def getTime(self):
        return time.strftime("%Y-%m-%d %T",time.localtime())
    def OnClose(self,event):
        sys.exit()
    def setButton(self,event):
        event.GetEventObject().SetLabel("最后更新时间:\n%s"%(self.getTime()))
        event.GetEventObject().SetSize((150,50))
    
    def OnDataClick0(self,event):
        self.showBalance()
        self.showJf()
        self.setButton(event)
        event.Skip()
    def OnDataClick1(self,event):
        self.showExInfo()
        self.setButton(event)
        event.Skip()
    def OnDataClick2(self,event):
        self.showPaiInfo()
        self.setButton(event)
        event.Skip()
    def OnDataClick3(self,event):
        self.showRefunding()
        self.setButton(event)
        event.Skip()

    def showJf(self):
        text=json.loads(urllib2.urlopen(jfUrl).read())
        self.item[10].SetLabel(str(text['point']))
        self.item[12].SetLabel(str(text['shopPromotion']))
    def showBalance(self):
        text=json.loads(urllib2.urlopen(balanceUrl).read())['data']
        self.item[4].SetLabel(text['balance'])
        self.item[6].SetLabel(text['totalQuotient'])
        self.item[8].SetLabel(text['totalProfit'])
    def createDataButton(self):
        for data in self.buttonData():
            self.Bind(wx.EVT_BUTTON,data[1],wx.Button(self.panel,-1,"刷新以上数据",pos=data[0],size=(-1,-1)))   
    def buttonData(self):
        y=200
        return [
                ((10,y),self.OnDataClick0),
                ((self.listItem[0].GetPositionTuple()[0],y),self.OnDataClick1),
                ((self.listItem[1].GetPositionTuple()[0],y),self.OnDataClick2),
                ((self.listItem[2].GetPositionTuple()[0],y),self.OnDataClick3),
                ]

    def labelData(self):
        x=5
        return [('宝贝物流信息:',(x,270)),
                ('淘宝用户名:',(x,30)),
                (unicode(self.tb.postData['TPL_username'],'gbk').encode('utf8'),(80+x,30)),
                ('支付宝余额:',(x,60)),
                ('        ',(80+x,60)),
                ('余额宝余额:',(x,90)),
                ('        ',(80+x,90)),
                ('余额宝收益:',(x,120)),
                ('        ',(80+x,120)),
                ('天猫积分余:',(x,150)),
                ('        ',(80+x,150)),
                ('店铺优惠卷:',(x,180)),
                ('        ',(80+x,180)),
                ('待收货:',(200+x,30)),
                ('待发货:',(360+x,30)),
                ('退货中:',(520+x,30)),

                ]
    def listData(self):
        w=120
        h=140
        pos=lambda (x,y):(x,y+30)
        return (
                (pos(self.item[-3].GetPositionTuple()),(w,h)),
                (pos(self.item[-2].GetPositionTuple()),(w,h)),
                (pos(self.item[-1].GetPositionTuple()),(w,h)),
                )
    def createList(self):    
        self.listItem=[]
        for data in self.listData():
            item=self.listItem.append(wx.ListBox(self.panel,-1,data[0],data[1],style=wx.LB_SINGLE))
            self.Bind(wx.EVT_LISTBOX_DCLICK,self.OnList,item)
    def OnList(self,event):
        item=event.GetEventObject()
        if item==self.listItem[0]:i=0
        elif item==self.listItem[1]:i=1
        else:i=2
        selectId=event.GetEventObject().GetSelection()
        data=self.payTime[i][selectId]
        name=event.GetEventObject().GetStringSelection().encode('utf8')
        mess="购买:%s\n花费:%s\n%s\n是否查看淘宝玉照?" %(name,data[1],data[0])
        
        dlg=wx.MessageDialog(self.panel,mess,name,style=wx.YES_NO ^wx.ICON_INFORMATION)
        if dlg.ShowModal() ==wx.ID_YES:
            imgFrame(window=self,pos=tuple([x+100 for x in self.GetPositionTuple()]),url=data[2]).Show()   

        #wx.Dialog(self.panel,-1,mess,name,style=wx.OK ).Show()

    def createLabel(self):
        self.item=[]#记录着各种标签
        for data in self.labelData():
            self.item.append(wx.StaticText(self.panel,-1,data[0],data[1]))
    def OnExClick(self,event):
        self.exText.Clear()
        event.GetEventObject().SetLabel("最后更新时间:%s"%(self.getTime()))
        event.GetEventObject().SetSize((250,28))
        event.Skip()
        self.showExInfo()
    def showPaiInfo(self):
        self.searchData={
                'auctionStatus':'PAID',
                'action':'itemlist/QueryAction',
                'user_type':'0',
                'event_submit_do_query':'1',
                'wrap':'bought-search-more',
                'auctionStatus':'PAID',
                'commentStatus':'ALL',
                'tradeDissension':'ALL',
                }
        post=urllib.urlencode(self.searchData)
        url=searchUrl+"&"+post
        names=self.tb.getName(url)
        self.payTime[1]=self.tb.getDealTime()
        self.listItem[-2].Clear()
        for name in names:
            self.listItem[-2].Append(name.strip())
    def showRefunding(self):
        self.searchData['auctionStatus']='REFUNDING'
        post=urllib.urlencode(self.searchData)
        url=searchUrl+"&"+post
        names=self.tb.getName(url)
        self.payTime[2]=self.tb.getDealTime()
        self.listItem[-1].Clear()
        for name in names:
            self.listItem[-1].Append(name.strip())
    def showExInfo(self):
        self.exText.Clear()
        self.listItem[-3].Clear()
        names=self.tb.getName(notUrl)
        urls=self.tb.getExUrl()
        self.payTime[0]=self.tb.getDealTime()
        for name in names:
            self.listItem[-3].Append(name.strip())
            exText=self.tb.getEX(urls[names.index(name)])
            self.exText.AppendText("*"*40 +name)
            try:
                self.exText.AppendText( exText['expressName'] + ":" + exText['expressId']+'\n')
                exInfo=exText['address']
                exInfo.reverse()
                for data in exInfo:
                     self.exText.AppendText(data['time'] + ":" + data['place']+'\n')
            except:
                self.exText.AppendText('无物流信息\n')
class loginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'请登录你的淘宝',size=(350,200),style=wx.CAPTION|wx.CLOSE_BOX)
        self.panel=wx.Panel(self,-1)
        userLabel=wx.StaticText(self.panel,-1,'账号: ',pos=(10,30),size=(50,-1))
        pwdLabel=wx.StaticText(self.panel,-1,'密码: ',pos=(10,60),size=(50,-1))
        self.userText=wx.TextCtrl(self.panel,-1,'qq929300079',pos=(userLabel.GetSize()[0],30),size=(150,-1))
        self.pwdText=wx.TextCtrl(self.panel,-1,'zxc12392930007',pos=(pwdLabel.GetSize()[0],60),size=(150,-1),style=wx.TE_PASSWORD)
        self.userText.SetFocus()
        self.checkText=wx.TextCtrl(self.panel,-1,"",pos=(240,60))
        self.checkLabel=wx.StaticText(self.panel,-1,"↑验证码↑",pos=(240,90))
        self.checkText.Show(False)
        self.button=wx.Button(self.panel,-1,'登录',pos=(30,120))
        self.Center()
        self.Show(True)
        self.tb=taobao()
        self.tb.getCheckCode()
        if self.tb.checkCodeUrl:
            self.showCheckCode()
        self.button.SetDefault()
        self.messLabel=wx.StaticText(self.panel,-1,'',pos=(10,160))
        self.Bind(wx.EVT_BUTTON,self.Click,self.button)
    
    def Click(self,event):
        user=self.userText.GetValue().encode('gbk')
        pwd=self.pwdText.GetValue().encode('gbk')
        self.tb.postData['TPL_username']=user
        self.tb.postData['TPL_password']=pwd
        if self.tb.checkCodeUrl:
            self.setCheckCode()
        mess=self.tb.loginTaobao()
        if not mess['state']:
            self.messLabel.SetLabel(mess['message'])
            self.tb.getCheckCode()
            self.showCheckCode()
            self.checkText.Clear()
        else:
            self.messLabel.SetLabel("登录成功，请等会儿。。")
            os.remove(CHECKFILE)
            self.Show(False)
            taobaoFrame(user,pwd).Show()           
            return False
            
    def showCheckCode(self):
        self.img=wx.Image(CHECKFILE,wx.BITMAP_TYPE_ANY)
        self.checkText.Show(True)
        self.checkCodeImg=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(self.img),pos=(240,30))
    def setCheckCode(self):
        self.tb.setCheckCode(self.checkText.GetValue())

class taobao(): 
    def __init__(self):
        self.postData = {
                'TPL_username':"",
                'TPL_password':"",
                'TPL_redirect_url':'http://www.taobao.com',  
                'callback':'1',  
                'css_style':'',  
                #  'event_submit_do_login':'anything',  
                'fc':'default',  
                'from':'tb',  
                'from_encoding':'',  
                'loginsite':'0',
                'guf':'',  
                'gvfdcname':'',  
                'isIgnore':'',  
                'longLogin':0,  
                'loginType':3,  
                'CtrlVersion': '1,0,0,7',  
                'minipara' :'',  
                'minititle':'',  
                'llnick':'',  
                'need_sign':'',  
                'need_user_id':'',  
                'not_duplite_str':'',  
                'poy':'',  
                'pstrong':'',  
                'sign':'',  
                'style':'default',  
                'support':'000001',  
                'tid':'',      
                'TPL_checkcode':'',
                'need_check_code':'',
                }
    def loginTaobao(self):
        return self.sendPost(url)
    def getCheckCode(self):
        try:
            taobao=urllib2.urlopen(url)
        except Exception,e:
                print '登录超时'
                sys.exit()

        page=taobao.read().decode('gbk')
        r_img=re.compile(r'codeURL:\"(.+?)\"')
        self.checkCodeUrl=r_img.findall(page)[0]
        fd=open(CHECKFILE,'wb')
        fd.write(urllib2.urlopen(self.checkCodeUrl).read())
        fd.close()
    def setCheckCode(self,checkCode):
        self.postData['TPL_checkcode']=checkCode
        self.postData['need_check_code']="true"
    def sendPost(self,url):
        post=urllib.urlencode(self.postData)
        req=urllib2.Request(url,post,hds)
        try:
            page=urllib2.urlopen(req,timeout=20)
        except urllib2.URLError,e:
            if isinstance(e.reason,socket.timeout):
                print '连接服务器超时'
                sys.exit()
        resultText=page.read().decode("gbk")
        page.close()
        resultText=json.loads(resultText)
        if  not resultText['state']:
            return resultText
        else:
            resultText['state']=True
            return resultText
    def getName(self,url):#获取宝贝名字
        req=urllib2.Request(url,None,hds)
        self.pageData=urllib2.urlopen(req).read().decode("gbk","ignore").encode('utf8')
        re_name=re.compile(r'<p class=\"baobei\-name\".*?>.+?<a.+?>(.+?)</a>',re.S)#匹配宝贝名字
        return re_name.findall(self.pageData)
    def getDealTime(self):
        re_time=re.compile(r'<span class=\"dealtime\">(.+?)</span>')
        re_pay=re.compile(r'<em class=\"real\-price.+?\">(.+?)</em>')
        #re_jpg=re.compile(r'<img.+?alt=.+?src=\"(http://.+?\.jpg).+?\"\/>')
        re_jpg=re.compile(r'<img.+?src=\"(http://.+?\.jpg).+?\"/>')
        return map(None,re_time.findall(self.pageData),re_pay.findall(self.pageData),re_jpg.findall(self.pageData))

    def getExUrl(self):
        AgoUrl='http://trade.taobao.com'#前缀，等下要加到查物流地址前的
        re_ExUrl=re.compile('data-url=\"(/.*?)\"')#匹配物流地址
        return [ AgoUrl+x for x in re_ExUrl.findall(self.pageData)]
#    def showExInfo(self):
#        re_name=re.compile(r'<a class=\"baobei\-name\".*?>(.+?)</a>',re.S)#匹配宝贝名字
#        names=self.getData(pageData,re_name)#获取匹配结果
#        classNames=self.get.Data(page)
#        EXurl=[ AgoUrl+x for x in self.getData(pageData,re_url)]#加上前缀
   #     for name in names:
   #         return name,
   #         self.getEX(EXurl[names.index(name)])
        
    def getEX(self,url):
        exText=json.loads(unicode(urllib2.urlopen(url).read(),'gbk').encode('utf8'))
        return exText
if __name__=='__main__':
    cookiejar=cookielib.LWPCookieJar()
    cookieSupport=urllib2.HTTPCookieProcessor(cookiejar)
    opener=urllib2.build_opener(cookieSupport,urllib2.HTTPHandler())
    urllib2.install_opener(opener)
    CHECKFILE=tempfile.mkstemp()[1]+'.jpg'
    app=wx.App()
    lFrame=loginFrame()
    app.MainLoop()
