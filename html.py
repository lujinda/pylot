#coding:utf8
import sys,re
from util import *
print "<html><head><title>...</title><body>"

htag="<%s>%s<%s>"

title=True
for block in blocks(sys.stdin):
    block=re.sub(r"\*(.+?)\*",r'<em>\1</em>',block)
    if title:
        print htag%("h1",block,"/h1")
        title=False
    else:
        print htag%("p",block,"/p")
