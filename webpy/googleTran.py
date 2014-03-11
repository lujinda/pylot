#coding:utf8
import urllib,urllib2,re,sys,time
header={'User-Agent':'chrome/28.0'}
url='http://translate.google.cn'
#proxy_h=urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})
#urllib2.install_opener(urllib2.build_opener(proxy_h))
def get_zORe(str):
	r_zORe=re.compile(u'[\u4e00-\u9fa5]+') #匹配中文
	if r_zORe.search(str.decode('utf8')):#需要把编码转成utf8才能匹配
		data={'sl':'zh-CN','tl':'en','js':'n','prev':'_t','hl':'zh-CN','ie':'UTF-8','text':str} #源语言为中文，目标语言为英语
	else:
		data={'sl':'en','tl':'zh-CN','js':'n','prev':'_t','hl':'zh-CN','ie':'UTF-8','text':str}#和上面的相反 
	return data
def get_tran(data):
	req=urllib2.Request(url,data,header)
	try:
		response=urllib2.urlopen(req).read()
	except Exception,e:
		print e
		sys.exit(1)
	response=unicode(response,'GBK').encode('utf8')#把中文编码改成utf8
	r_tran=re.compile(r'TRANSLATED_TEXT=\'(.+)\';INPUT',re.L)
	return r_tran.findall(response)[0].replace("\\x26#39;",'\'')
if __name__ == '__main__':
	try:
		str=sys.argv[1]
	except IndexError,e:
		print '使用方法:程序名+一句中文或英语，如果有空格，请使用引号将字符串引起来'
		sys.exit(1)
	data=urllib.urlencode(get_zORe(str))
	print str + ': ' +get_tran(data)
	sys.exit()
