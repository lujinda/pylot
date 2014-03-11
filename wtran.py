import googleTran,web
fd=open(sys.argv[1],'r')
for i in fd.readlines():
	 text=i.rstrip('\n')
	 print text
	 print googleTran.get_tran(urllib.urlencode(googleTran.get_zORe(text)))

