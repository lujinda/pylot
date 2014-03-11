import re
import urllib2
def getHtml(url):
	page=urllib2.urlopen(url)
#	return page

#def getImg(page):
#	r_img=re.compile(r"src=\"((http://|).+\.(jpg|png|gif))\"",re.I)
#	for URL in  r_img.findall(page):
#		if not URL[1]:
#			URL=Url+'/'+URL[0]
#		else:
#			URL=URL[0]
#		fileName=URL.split('/')[-1]
#		urllib.urlretrieve(URL,fileName)

Url=raw_input("Input URL:")
#try:
#	os.mkdir('img')
#except OSError,e:
#	if e.errno == 17:
#		pass
#	else:
#		print e
#		sys.exit()
os.chdir('img')
page=getHtml(Url)

