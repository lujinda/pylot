#!/usr/bin/env python
import re
fd=open('/proc/meminfo','r')
result=fd.readlines()[0:4]
text=str(result)
data=re.findall(r'([0-9]+)',text)
data=[int(x) for x in data ]
print format(sum(data[1:])*1.0/data[0],'0.2%')
