import googleTran,sys,urllib
fd=open(sys.argv[1],'r')
data=fd.readlines()
data=[ x for x in data if x!='\n' ]
for i in data:
	text=i.rstrip('\n')
	print text
	print googleTran.get_tran(urllib.urlencode(googleTran.get_zORe(text)))

