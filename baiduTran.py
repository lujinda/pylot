#coding:utf8
import urllib,urllib2,sys
import json
def tran(mess):
	clientId='client_id=OrVMSfSKtvo9h59DZlGyGhRI'
	apiUrl='http://openapi.baidu.com/public/2.0/bmt/translate?'
	url="%s%s&q=%s&from=auto&to=auto" %(apiUrl,clientId,mess)
	Dstr=json.loads(urllib2.urlopen(url).read())
#	print urllib2.urlopen(url).read()
	return Dstr['trans_result'][0]['dst']
try:
	sStr=sys.argv[1]
except IndexError,e:
	print '使用方法，程序+您想要翻译的内容～'
	sys.exit()
print tran(sStr)

