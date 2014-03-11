#!/usr/bin/env python
#coding:utf8
url='http://translate.google.cn/'
import wx,urllib,urllib2,re,threading
hds={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
postData={
'sl':'',
'tl':'',
'js':'n',
'prev':'_t',
'hl':'zh-CN',
'ie':'UTF-8',
'text':'',
}
sl={'中文':'zh-CN','英语':'en','阿尔巴尼亚语':'sq','马来语':'ms','白俄罗斯语':'be','拉丁语':'la','意大利语':'it','克罗地亚语':'hr','日语':'ja','瑞典语':'sv','希腊语':'el','苗语':'hmn','索马里语':'so','威尔士语':'cy','印尼语':'id','乌尔都语':'ur','希伯来语':'iw','罗马尼亚语':'ro','捷克语':'cs','爱沙尼亚语':'et','海地克里奥尔语':'ht','古吉拉特语':'gu','南非祖鲁语':'zu','马其顿语':'mk','高棉语':'km','中文(简体)':'zh-CN','丹麦语':'da','巴斯克语':'eu','印地语':'hi','马拉地语':'mr','蒙古语':'mn','旁遮普语':'pa','阿拉伯语':'ar','卡纳达语':'kn','泰米尔语':'ta','宿务语':'ceb','约鲁巴语':'yo','保加利亚语':'bg','西班牙语':'es','斯瓦希里语':'sw','匈牙利语':'hu','马耳他语':'mt','波斯语':'fa','冰岛语':'is','土耳其语':'tr','意第绪语':'yi','尼泊尔语':'ne','孟加拉语':'bn','菲律宾语':'tl','世界语':'eo','法语':'fr','毛利语':'mi','伊博语':'ig','加泰罗尼亚语':'ca','斯洛文尼亚语':'sl','越南语':'vi','立陶宛语':'lt','拉脱维亚语':'lv','塞尔维亚语':'sr','德语':'de','亚美尼亚语':'hy','韩语':'ko','泰语':'th','荷兰语':'nl','葡萄牙语':'pt','爱尔兰语':'ga','中文(繁体)':'zh-TW','斯洛伐克语':'sk','挪威语':'no','老挝语':'lo','布尔语(南非荷兰语)':'af','乌克兰语':'uk','泰卢固语':'te','印尼爪哇语':'jw','芬兰语':'fi','波斯尼亚语':'bs','格鲁吉亚语':'ka','豪萨语':'ha','波兰语':'pl','阿塞拜疆语':'az','加利西亚语':'gl','俄语':'ru'}
class t_tranText(threading.Thread):
    def __init__(self,window):
        threading.Thread.__init__(self)
        self.window=window
        self.start()
    def run(self):
        wx.CallAfter(self.window.tranText)
class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,title='疯狂谷歌小翻译(q8886888@qq.com))',size=(700,320),style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)
        self.panel=wx.Panel(self)
        wx.StaticText(self.panel,-1,'源语言:',pos=(10,15))
        wx.StaticText(self.panel,-1,'目标语言:',pos=(350,15))
        self.sText=wx.TextCtrl(self.panel,-1,'',pos=(10,40),size=(300,250),style=wx.TE_MULTILINE)
        self.sText.SetFocus()
        self.dText=wx.TextCtrl(self.panel,-1,'',pos=(350,40),size=(300,250),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.button=wx.Button(self.panel,-1,'→',pos=(310,160),size=(40,30))
        self.button.SetDefault()
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.button)
        self.sText.Bind(wx.EVT_KEY_UP,self.OnUp)
        self.createSlList()
        isTop=wx.CheckBox(self.panel,-1,"窗口最前",pos=(10,290))
        self.Bind(wx.EVT_CHECKBOX,self.swTop,isTop)
        self.Center()
        self.Show()
    def swTop(self,event):
        Value=event.GetEventObject().GetValue()
        if Value:
            self.SetWindowStyle(self.GetWindowStyle() |wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(self.GetWindowStyle() ^wx.STAY_ON_TOP)
    def OnUp(self,event):
        if event.GetKeyCode()==13 :self.tranText()
    def tranText(self):
        self.button.Enable(False)
        self.SetTitle('翻译中，请稍等～')
        self.dText.Clear()
        try:
            postData['sl']=sl[self.listItem[0].GetValue().encode('utf8')]
            postData['tl']=sl[self.listItem[1].GetValue().encode('utf8')]
            postData['text']=str(self.sText.GetValue().encode('utf8').rstrip('\n'))
        #print postData['text']
            data=urllib.urlencode(postData)
            r_tran=re.compile(r'TRANSLATED_TEXT=\'(.*?)\';INPUT',re.L)
            req=urllib2.Request(url,data,hds)
            result=urllib2.urlopen(req).read()
            self.dText.write(r_tran.findall(result)[0].replace("\\x26#39;",'\'').replace("\\x3cbr\\x3e",'\n'))   
            self.SetTitle('翻译成功～')

        except:
            self.SetTitle('翻译失败～')
        finally:
            self.button.Enable(True)
    def OnClick(self,event):
        t_tranText(self)
    def listData(self):
        return (
                ('检测语言',(60,10)),
                ('英语',(410,10)),
                )
    def createSlList(self):
        self.listItem=[]
        for data in  self.listData():
            sampleList=[]
            for d in sorted(sl.keys()):
                sampleList.append(d)
            self.listItem.append(wx.ComboBox(self.panel,-1,data[0],data[1],(140,-1),sampleList,wx.CB_DROPDOWN|wx.CB_READONLY))
        
        sl['检测语言']='auto'
        

if __name__=='__main__':
    app=wx.App()
    frame=myFrame()
    app.MainLoop()
