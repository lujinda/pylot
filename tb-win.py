#coding:gbk
"""
���ֱ���������˵����
notUrl�����ַ����ȷ���ջ���ҳ���ַ
post�Ǿ�postData,urlencode���
ex��ʾ�ſ�ݵ���˼��getCheckCode������������֤�뵽���أ�Ȼ�����û��Լ�����
showExInfo()������ʾδȷ���ջ�������������Ϣ(��ʵgetExInfo���ǣ���ֻ��ΪgetExInfo�ṩ�ˣ�����Ҫ������,��������ʾ��������)��getExInfo()��ʾ��Ӧ������������Ϣ
"""
import urllib,urllib2,cookielib,re,json
import tempfile
import os
import xml.etree.ElementTree as et
import random
import atexit
import sys
import threading
import getpass
import itertools
IMGNAME="_taobao_t.jpg"

hds={
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
}
idUrl="http://try.taobao.com/json/ajaxGetUserAddress.htm?&_input_charset=utf-8&only=true"
url='https://login.taobao.com/member/login.jhtml'#��¼��ַ,login address
class taobao(): 
    def __init__(self,pwd):
        atexit.register(exiting)
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
			fd=open("tb.xml")
			xmlText=fd.read().decode("gbk").encode("utf-8") # python��xml��֧��gbk��gb2312�������Ҵ�����utf8����gbk�洢����utf-8����
			fd.close()
			root=et.fromstring(xmlText)
			self.fWord=root.find("word").text
			self.username=root.find("name").text
			self.Max=int(root.find("max").text)
			self.Min=int(root.find("min").text)
        except Exception,e:
			print e
			print "tb.xml���ò����ڣ�����������Ŷ!"
			sys.exit(1)

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
        fd=open("%s"%IMGNAME,'wb')
        fd.write(urllib2.urlopen(url).read())
        fd.close()
        t=threading.Thread(target=self.showImg)
        t.setDaemon(True)
        t.start()
        checkCode=raw_input('��������֤�룬��֤����(��ǰĿ¼%s):'%IMGNAME)
        self.postData['TPL_checkcode']=checkCode
        self.postData['need_check_code']="true"

    def showImg(self):
        try:
		    os.system(IMGNAME)
        except:
            pass

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
            print "��¼�ɹ�!"
            self.showInfo()
    
    def showInfo(self):
        #self.readInfo()
        urls=itertools.imap(lambda x:"http://try.taobao.com/item/newItemList.htm?tab=2&page=%d&anchor=true&_input_charset=utf-8" %x,range(2,100))
        try:
            for url in urls:
                if self.connter>50:
                    break
                self.readPage(url)
        except KeyboardInterrupt:
            print "Bye!!\n����ɹ�%d��..."%self.connter

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
            postUrl="http://try.taobao.com/json/pre_apply.do?_tb_token_=%s&q=%s&a=%s&itemId=%s&_input_charset=utf-8"%(token,urllib.quote(q),urllib.quote(a),itemId)
            msg=json.loads(urllib2.urlopen(postUrl).read())
            if msg["isSuccess"]:
                idPage=json.loads(urllib2.urlopen(idUrl).read().decode("gbk"))
                addId=idPage["data"][0]["id"]
                self.sendAdd(itemId,msg["_tb_token_"],q,a,addId)
                self.connter+=1
                print "Ok"
        except Exception,e:
            print "Error!"
    
    def sendAdd(self,itemId,token,q,a,addId):
        url="http://try.taobao.com/json/apply.do?_tb_token_=%s&q=%s&a=%s&itemId=%s&&_input_charset=utf-8&addressId=%s&from=matrixtry&pageId=0&moduleId=0" %(token,urllib.quote(q),urllib.quote(a),itemId,addId)
        urllib2.urlopen(url)

    def urlDecode(self,value):
        return re.sub(r"&#(\d+);",lambda x:unichr(int(x.group(1))),value)

if __name__=='__main__':
    def exiting():
        os.system("pause")
    os.system("color %s"%random.choice(["3F","2F","1F","1B","0F"]))
    os.system("title ����:³��� �̺�:670913")
    print "��ӭʹ�á��Ա���������á����������������ϵ��(����С���)"
    password=getpass.getpass()
    tb=taobao(password)
    tb.loginTaobao()
    
