#coding:utf8
import sys,re,urllib,urllib2,cookielib,os.path,json
cookie=cookielib.LWPCookieJar()
chandle=urllib2.HTTPCookieProcessor(cookie)
def getData(url):
	r=urllib2.Request(url)
	opener=urllib2.build_opener(chandle)
	u=opener.open(r)
	data=u.read()
	try:
		data=data.decode('utf-8')
	except:
		data=data.decode('gbk','ignore')
	return data
def postData(url,data):
	data=urllib.urlencode(data)
	data=bytes(data)
	r=urllib2.Request(url,data)
	opener=urllib2.build_opener(chandle)
	u=opener.open(r)
	data=u.read()
	try:
		data=data.decode('utf-8')
	except:
		data=data.decode('gbk','ignore')
	return data
class Baidu:
   def __init__(self,name,pwd):
        url='http://www.baidu.com'
        getData(url)
        par={
            "apiver":'v3',
            "callback":'bd__cbs__oug2fy',
            "class":'login',
            "logintype":'dialogLogin',
            "tpl":'tb',
            "tt":'1385013373144'
        }
        url='https://passport.baidu.com/v2/api/?getapi&%s' % urllib.urlencode(par)
        token=re.findall('"token" : "(.*?)"',getData(url))[0]
        par.update({"isphone":'false',"username":name,"token":token})
        url='https://passport.baidu.com/v2/api/?logincheck&%s' % urllib.urlencode(par)
        data={
            "charset":'GBK',
            "mem_pass":'on',
            "password":pwd,
            "ppui_logintime":'1612376',
            "quick_user":'0',
            "safeflg":'0',
            "splogin":'rate',
            "u":'http://tieba.baidu.com/'
        }
        url='https://passport.baidu.com/v2/api/?login'
        par.update(data)
        bdu=re.findall('hao123Param=(.*?)&',postData(url,par))[0]
        par={
            "bdu":bdu,
            "t":'1385013373144'
        }
        url='http://user.hao123.com/static/crossdomain.php?%s' % urllib.urlencode(par)
        getData(url)
        #获取个人信息
        info=json.loads(getData('http://tieba.baidu.com/f/user/json_userinfo'))
        print info
        self.name=info['data']['user_name_show']
        #获取页数
        url='http://tieba.baidu.com/f/like/mylike'
        cont=getData(url)
#       page=int(max(re.findall('<a href="/f/like/mylike\?\&pn=\d+">(\d+)</a>',cont)))
        print("%s，%s" % ("你好", urllib.urlencode(self.name.decode('utf8'))))
        print("----------------------------------")
        self.sign(page)
    #签到
	def sign(self,page):
		i=1
        while i <= page:
            url='http://tieba.baidu.com/f/like/mylike?&pn=%d' % i
            for x in re.findall('<a href="([^<]+?)" title="([^<]+?)">', getData(url)):
                url='http://tieba.baidu.com%s' % x[0]
                tbs=re.findall('PageData.tbs = "(.+?)"', getData(url))[0]
                url='http://tieba.baidu.com/sign/add'
                par={
                    "ie":'utf-8',
                    "kw":x[1],
                    "tbs":tbs
                }
                js = json.loads(postData(url, par))
                tip = js["error"]
                if tip == "":
                    tip = "签到成功"
                print("%s吧：%s" % (x[1], tip))
            i+=1
        print("---------------END----------------")
        print("亲，记得明天再来噢")

baidu=Baidu('qq929300079','zxc123')
