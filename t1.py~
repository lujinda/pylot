import parse
fd=open("out.txt",'a+')
import os
for filename in os.popen("ls *.flv").readlines():
    parse.parseVedio(None,fd,filename.strip())
