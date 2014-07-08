#coding:utf8
fd=open("/web/lupa/videos.txt")
wfd=open("list.txt",'w')
s="http://v.youku.com/v_show/id_%s.html"
for line in fd:
    line=line.split(',')[1].strip()
    url=s%line
    wfd.write(url+'\n')
    
wfd.close()
    
    
