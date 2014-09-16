#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-28 15:01:45
# Filename        : t1.py
# Description     : 
import re
import sys
import time
TXTPATH="/home/ljd/py/utf-8.txt"

start_time=time.time()

def convert(zh):
    assert(isinstance(zh,unicode))
    re_zh=re.compile(u"[\u4e00-\u9fa5]")
    if not re_zh.search(zh):return zh
    try:
        words=open(TXTPATH,'r')
        for line in words:
            line=line.strip().decode("utf-8")
            word,pinyin=line[0].strip(),line[1:]
            if zh==word:
                return pinyin.split(',')[0][:-1]
        return zh
    except OSError,e:
        sys.exit(1)
    finally:
        words.close()

if __name__=="__main__":
    fd=open('亮剑.txt','r')
    for line in fd:
        line=line.decode("utf-8")
        words=map(convert,line)
        print ' '.join(words)
    print time.time()-start_time
        
