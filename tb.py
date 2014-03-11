# -*- coding: utf-8 -*-
"""
部分变量，函数说明：
notUrl这个地址是特确认收货的页面地址
post是经postData,urlencode后的
ex表示着快递的意思，getCheckCode是用来下载验证码到本地，然后由用户自己输入
showExInfo()用来显示未确认收货宝贝的物流信息(其实getExInfo才是，它只是为getExInfo提供了，所需要的数据,它用来显示宝贝名字)，getExInfo()显示对应宝贝的物流信息
"""
import urllib,urllib2,chardet,cookielib,re,json
hds={
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
}
 
url='https://login.taobao.com/member/login.jhtml'#登录地址,login address
notUrl='http://trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1&auctionStatus=SEND'#这是待确认收货地址
#username=raw_input('请输入用户:')
#password=raw_input('请输入密码:')
class taobao(): 
    def __init__(self,user,pwd):
        self.postData = {
                'TPL_username':unicode(user,'utf8').encode('gbk'),
                'TPL_password':pwd,
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
        cookiejar=cookielib.LWPCookieJar()
        cookieSupport=urllib2.HTTPCookieProcessor(cookiejar)
        opener=urllib2.build_opener(cookieSupport,urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        taobao=urllib2.urlopen(url)
        page=taobao.read().decode('gbk')
        r_img=re.compile(r'codeURL:\"(.+?)\"')
        checkCodeUrl=r_img.findall(page)[0]
        if checkCodeUrl:
            self.getCheckCode(checkCodeUrl)
            self.sendPost(url)
    def getCheckCode(self,url):
        fd=open("/data/_taobao_t.jpg",'wb')
        fd.write(urllib2.urlopen(url).read())
        fd.close()
        checkCode=raw_input('请输入验证码，验证码在(/data/_taobao_t.jpg):')
        self.postData['TPL_checkcode']=checkCode
        self.postData['need_check_code']="true"
    def sendPost(self,url):
        post=urllib.urlencode(self.postData)
        req=urllib2.Request(url,post,hds)
        page=urllib2.urlopen(req)
        resultText=page.read().decode("gbk")
        page.close()
        resultText=json.loads(resultText)
        if  not resultText['state']:
            print resultText['message']
        else:
            self.showExInfo()
    def showExInfo(self):
        AgoUrl='http://trade.taobao.com'#前缀，等下要加到查物流地址前的
        pageData=unicode(urllib2.urlopen(notUrl).read(),'gbk').encode('utf8')
        re_name=re.compile(r'<a class=\"baobei\-name\".*?>(.+?)</a>',re.S)#匹配宝贝名字
        re_url=re.compile(r'<a href=.*?data\-url=\"(/.*)\">')#匹配物流地址
        names=self.getData(pageData,re_name)#获取匹配结果
        EXurl=[ AgoUrl+x for x in self.getData(pageData,re_url)]#加上前缀
        for name in names:
            print name,
            self.getEX(EXurl[names.index(name)])
        
    def getEX(self,url):
        exText=json.loads(unicode(urllib2.urlopen(url).read(),'gbk').encode('utf8'))
        try:
            print exText['expressName'] +":" +exText['expressId']
            exInfo=exText['address']
            exInfo.reverse()
            for data in exInfo:
                print data['time']+":" +data['place']
        except:
            print '无物流信息'
    def getData(self,data,re_data):
        return re_data.findall(data)
if __name__=='__main__':
    tb=taobao('912766762aqq','yulipingzxc123')
    tb.loginTaobao()
    
