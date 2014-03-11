#coding:utf8
import urllib2
import urllib
import cookielib
import re
import sys
import random
import mimetypes
import mimetools
account=[]
reg_url='http://bbs.ph66.com/register.php?forward=http%3A%2F%2Fapps.ph66.com%2Fmodule%2Fvote%2Fcontent%2F%3Fid%3D34%26gid%3D163%26fied%3Dstat%26sort%3D%26page%3D2'
add_url='http://apps.ph66.com/module/vote/content/?mode=&fied=&sort=&action=post&id=34'
page_url='http://apps.ph66.com/module/vote/content/?id=34&gid=163&fied=stat&sort=&page=2'
addInfo=[]
hds={
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Referer':'http://bbs.ph66.com/register.php',
        }
regInfo={
        'forward':'',
        'regname':None,
        'regpwd':'zxc123',
        'regpwdrepeat':'zxc123',
        'regemail':None,
        'field_3':'130',
        'gdcode':None,
        'step':'2',
        'rgpermit':'1',
        
        }
def mkUser():
    username=''
    for i in range(random.randint(6,15)):#生成一个由数字字母组成的6到15位用户名
        username+=str(random.choice(username_data))
    return username
def mkEmail(username):
    return username + '@' +str(random.choice(email_data))#生成用户名+邮箱后缀的邮箱地址
    
class regUser():
    def __init__(self):
        cj=cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        self.getSessionid()
        mkUser()
        regInfo['regname']=mkUser()
        regInfo['regemail']=mkEmail(regInfo['regname'])
        self.getCode()
        self.entryCode()
        self.regData=urllib.urlencode(regInfo)
        self.regUser(('http://bbs.ph66.com/register.php?','http://bbs.ph66.com/register.php?step=finish'))
        account.append((regInfo['regname'],regInfo['regpwd']))        
        self.addSocre()
    def getCode(self):
        img_url='http://pin.aliyun.com/get_img?identity=bbs.ph66.com&kjtype=default&sessionid='+self.sessionid
        urllib.urlretrieve(img_url,'checkcode.png')
    def addSocre(self):
        addhds={
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Content-Type':'multipart/form-data; boundary=---------------------------7de1db1017c',
        'Host':'apps.ph66.com',
        'Connection':'Keep-Alive',
        'Cache-Control':'no-cache',
        }
        addInfo.append('-----------------------------7de1db1017c')
        addInfo.append('Content-Disposition: form-data; name="keys"')
        addInfo.append('')
        addInfo.append(self.getKey())
        addInfo.append('-----------------------------7de1db1017c')
        addInfo.append('Content-Disposition: form-data; name="G-163[]"')
        addInfo.append('')
        addInfo.append('932')
        addInfo.append('-----------------------------7de1db1017c--')
        body='\r\n'.join(addInfo)
        req=urllib2.Request(add_url,body,addhds)
        urllib2.urlopen(req)
    def getKey(self):
        re_key=re.compile(r'value=\'(.+?)\' name=\'keys\'')
        page=urllib2.urlopen(page_url).read()
        return re_key.findall(page)[0]

    def entryCode(self):
        regInfo['gdcode']=raw_input('请输入验证码:')
    def regUser(self,urls):
        for url in urls:
            req=urllib2.Request(url,self.regData,hds)
            conn=urllib2.urlopen(req)
        conn.close()
    def getSessionid(self):
        re_sessionid=re.compile(r'sessionid=(.+?)\"')
        req=urllib2.Request(reg_url,None,hds)
        page=urllib2.urlopen(req).read()
        self.sessionid=re_sessionid.findall(page)[0]
if __name__=='__main__':
    username_data=[chr(x) for x in range(97,123)]+range(0,10) #生成0-9 a-z
    email_data=['qq.com','126.com','163.com','189.cn','yahoo.cn']#生成邮箱的，随机取一个后缀
    while True:
        try:
            reguser=regUser()
        except:
            sys.exit()
    print account
    
