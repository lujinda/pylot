# -*- coding: utf-8 -*-
import urllib,urllib2,cookielib,re,json
import threading
import tempfile
import xml.etree.ElementTree as et
import sys
import getpass
import atexit
import itertools

hds={
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
}
idUrl="http://try.taobao.com/json/ajaxGetUserAddress.htm?&_input_charset=utf-8&only=true"
url='https://login.taobao.com/member/login.jhtml'#登录地址,login address
class taobao(): 
    def __init__(self,pwd):
        self.setValue()
        self.postData = {
                'TPL_username':self.username.encode('gbk'),
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
        self.connter=0

    def setValue(self):
        try:
            tree=et.parse("tb.xml")
            root=tree.getroot()
            self.fWord=root.find("word").text
            self.username=root.find("name").text
            self.Max=int(root.find("max").text)
            self.Min=int(root.find("min").text)
        except:
            print "tb.xml配置不存在，或配置有误哦!"
            sys.exit(1)

    def loginTaobao(self):
        cookiejar=cookielib.LWPCookieJar()
        self.c=cookiejar
        cookieSupport=urllib2.HTTPCookieProcessor(cookiejar)
        opener=urllib2.build_opener(cookieSupport,urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        taobao=urllib2.urlopen(url)
        page=taobao.read().decode('gbk')
        r_img=re.compile(r'codeURL:\"(.+?)\"')
        try:
            checkCodeUrl=r_img.findall(page)[0]
        except IndexError:
            checkCodeUrl=''
        if checkCodeUrl:
            self.getCheckCode(checkCodeUrl)
        self.sendPost(url)
    def getCheckCode(self,url):
        fd=open("_taobao_t.jpg",'wb')
        fd.write(urllib2.urlopen(url).read())
        fd.close()
        checkCode=raw_input('请输入验证码，验证码在(当前目录_taobao_t.jpg):')
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
            print "登录成功!"
            self.getTbToken()
            self.showInfo()
    
    def getTbToken(self):
        url="http://trade.taobao.com/trade/itemlist/list_bought_items.htm"
        req=urllib2.urlopen(url)
        self.token=re.findall(r".+name=\"_tb_token_\" value=\"(.+?)\"",req.read())[0]
        req.close()

    def showInfo(self):
        #self.readInfo()
        self.t_getUid=threading.Thread(target=self.getUid)
        self.t_getUid.start()
        urls=itertools.imap(lambda x:"http://try.taobao.com/item/newItemList.htm?tab=2&page=%d&anchor=true&_input_charset=utf-8" %x,range(2,100))
        try:
            for url in urls:
                if self.connter>50:
                    break
                self.readPage(url)
        except KeyboardInterrupt:
            print "Bye!!\n申请成功%d件..."%self.connter
            self.t_getUid.join()
            try:
                tryData=self.getTryCard()
                print u"总申请:%s,成功:%s\n总报告:%s,精华:%s\n淘宝等级:Lv %s,试用豆:%s" \
                    %(tryData["requestNum"],tryData["successNum"]
                            ,tryData["reportsNum"],tryData["primeReportNum"],
                            tryData["level"],tryData["tryBeansNum"]
                            )
            except:
                pass
            sys.exit(0)

    def getUid(self):
        url="http://trade.taobao.com/trade/itemlist/list_bought_items.htm"
        req=urllib2.Request(url,None,hds)
        page=urllib2.urlopen(req)
        re_userid=re.compile(r"userid=(\d+)")
        self.userid=re_userid.findall(page.read())[0]
        page.close()
        
        
    def getTryCard(self):
        url="http://try.taobao.com/json/try_user_card.htm?user_id=%s&_input_charset=utf-8" %self.userid
        jsonData=urllib2.urlopen(url).read().decode("gbk")
        return json.loads(jsonData)["data"]
    
        

    def readPage(self,itemUrl):
        req=urllib2.Request(itemUrl,None,hds)
        page=urllib2.urlopen(req).read()
        resultText=json.loads(page)
        for data in resultText["below"]["data"]:
            title=self.urlDecode(data["title"])
            jiage=int(data["currentPrice"])
            if self.Min <= jiage <=self.Max and \
                    (not re.search(u"%s"%("|".join(self.fWord)),
                        title)):
                print title,jiage
                self.readItem(data["itemDetailUrl"])

    def readItem(self,url):
        req=urllib2.Request(url,None,hds)
        page=urllib2.urlopen(req).read()
        itemId=re.findall(r"id=(\d+)",url)[0]
        token=re.findall(r"<input name=\'_tb_token_\'.+value=\'(.+)\'>",page)[0]
        r_q=re.compile(r"<div class=\"question\".+<em>(.+?)</em>.+<a href=\"(.+)\" target=\"_blank\">.+</div>")
        que,url=r_q.findall(page)[0]
        self.findA(que,url,itemId,token)

    def findA(self,que,url,itemId,token):
        page=urllib2.urlopen(url).read()
        try:
            try:
                a,q=re.findall(r"<li .*title=\"&nbsp;(.+)\">(%s):" %repr(que)[1:-1],page)[0]
                a=self.urlDecode(a).encode("utf8")
                q=q.decode("gbk").encode("utf8")
            except:
                a,q=re.findall(r"<li .*title=\" (.+)\">(%s):" %que.decode("gbk"),page.decode("gbk"))[0]
                a=a.encode("utf8")
                q=q.encode("utf8")
            finally:
                self.shopId=re.findall(r"shopId:\"(\d+)\"",page)[0]
                self.itemId=re.findall(r"itemId:\"(\d+)\"",page)[0]
            postUrl="http://try.taobao.com/json/pre_apply.do?_tb_token_=%s&q=%s&a=%s&itemId=%s&_input_charset=utf-8"%(token,urllib.quote(q),urllib.quote(a),itemId)
                
            msg=json.loads(urllib2.urlopen(postUrl).read())
            if msg["isSuccess"]:
                idPage=json.loads(urllib2.urlopen(idUrl).read().decode("gbk"))
                addId=idPage["data"][0]["id"]
                self.sendAdd(itemId,msg["_tb_token_"],q,a,addId)
                self.connter+=1
                print "Ok"
        except Exception,e:
            print "Error"
    
    def sendAdd(self,itemId,token,q,a,addId):
        url="http://try.taobao.com/json/apply.do?_tb_token_=%s&q=%s&a=%s&itemId=%s&&_input_charset=utf-8&addressId=%s&from=matrixtry&pageId=0&moduleId=0" %(token,urllib.quote(q),urllib.quote(a),itemId,addId)
        self.addFav()
        urllib2.urlopen(url)
    
    def addFav(self):
        url="http://favorite.taobao.com/popup/add_collection.htm"
        for postData in self.mkFavPost():
            hds={
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
        "Origin":"http://favorite.taobao.com",
        "Referer":"http://favorite.taobao.com/popup/add_collection_2.htm?id=%s&itemtype=%s&is_tmall="%(postData["id"],postData["itemtype"])
            }
            req=urllib2.Request(url,urllib.urlencode(postData),hds)
            urllib2.urlopen(req)
        
    
    def mkFavPost(self):
        return map(lambda x,y:dict([("itemtype",x),
            ("id",y),
            ("_tb_token_",self.token)]),
            map(str,range(2)),(self.shopId,self.itemId))

    def urlDecode(self,value):
        return re.sub(r"&#(\d+);",lambda x:unichr(int(x.group(1))),value)

if __name__=='__main__':
    password=getpass.getpass()
    tb=taobao(password)
    tb.loginTaobao()
    
