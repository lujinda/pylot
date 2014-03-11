import urllib2 

def Login(lgurl):
	try:
		page=urllib2.urlopen(lgurl).read()
		print page
	except urllib2.HTTPError,e:
		if int(e.code) == 401:
			inKey(lgurl)
		else:
			print e
def inKey(lgurl):
	passMgr=urllib2.HTTPPasswordMgrWithDefaultRealm()
	passMgr.add_password(None,lgurl,raw_input('Please input username:'),raw_input('Please input key:'))
	handler=urllib2.HTTPBasicAuthHandler(passMgr)
	urllib2.install_opener(urllib2.build_opener(handler))
	Login(lgurl)
Login('http://172.16.0.5:8080')
