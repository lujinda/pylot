from urllib2 import *
num=int(raw_input("input num:"))
url=raw_input("input url:")
hds = {'User-Agent':' Chrome/28.0.1500.72'}
req=Request(url,None,hds)
for i in range(1,num+1):
	print i
	my=urlopen(req)
	my.close()
	
