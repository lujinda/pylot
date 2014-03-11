#coding:utf8
import urllib,urllib2,re,sys
fd=open('citylist.txt','r')
try:
	city=sys.argv[1]
except IndexError,e:
	city='绍兴'
data=fd.read()
r_c=re.compile(u'' + city)
print r_c.findall(data)
#w_url='http://m.weather.com.cn/data/%s.html' %()
#c_data=f
