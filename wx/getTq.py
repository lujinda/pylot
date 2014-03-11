#coding:utf8
#环境:
import urllib,urllib2,sys,re
def toUtf8(str):#用来正确显示中文的函数
	return unicode(str,'gb2312').encode('utf8').rstrip()
	
try:
	city=urllib.quote(unicode(sys.argv[1],'utf8').encode('gb2312'))
except IndexError,e:
	city=urllib.quote(unicode('绍兴','utf8').encode('gb2312'))
def getPage():
	w_url='http://sogou.soso.com/tb.q?cid=tb.tq&cin=&city=' + city #以上几步在生成地址
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'} 
	w_req=urllib2.Request(w_url,None,headers)
	try:
		w_page=urllib2.urlopen(w_req,timeout=4).read()#把页面读下来，超时为4秒
	except Exception,e:
		print e#如果超时，则打印出来,ps:我这网络不给力，总是超时,换了个网络环境就没有超时过了
		sys.exit(1)
	return w_page
w_page=getPage()
if city == 'help':
	w_page=unicode(w_page,'gb2312').encode('utf8')
	r_all=re.compile(u'p2c\s*=\s*\{(.+?)\}',re.S)
	aData=r_all.findall(w_page)[0]
	print aData.replace('\'','').replace(',',' ').replace('eof:[]','').rstrip()
else:
	r_weath=re.compile(r'<!\[CDATA\[(.+)\]\]>')#正则规划
	w_data=r_weath.findall(w_page)#把数据匹配出来
	print toUtf8(w_data[0]) + '---' + toUtf8(w_data[1])
	day=['今天','明天','后天']
	for i in range(3):
		map=[2,3,4]
		print  '%s: %s\t%s,%s' %(day[i],toUtf8(w_data[map[0]+i*3]),toUtf8(w_data[map[1]+i*3]),toUtf8(w_data[map[2]+i*3]))
