#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-28 08:05:03
# Filename        : toPinyin.py
# Description     : 
import re
import sys
TXTPATH="/home/ljd/py/utf-8.txt"
cache_word={}

class ToPinYin():
    def __init__(self):
        self.to_pinyin=self.__convert()
        self.to_pinyin.next()

    def convert(self,word):
        return self.to_pinyin.send(word)

    def __convert(self):
        zh=yield None
        assert(isinstance(zh,unicode))
        re_zh=re.compile(u"[\u4e00-\u9fa5]")
        try:
            words=open(TXTPATH,'r')
            for line in words:
                line=line.strip().decode("utf-8")
                word,pinyin=line[0],line[1:]
                pinyin=pinyin.split(',')[0][:-1]
                cache_word[word]=pinyin
                if zh==word:
                    zh=yield pinyin
                if not re_zh.search(zh):zh=yield zh
            yield None
        except OSError,e:
            sys.exit(1)
        finally:
            words.close()
            yield

if __name__=="__main__":
    pinyin=ToPinYin()
    while True:   
        line=raw_input("请输入中文：").decode("utf-8")
        if not line:break
        words=[cache_word.get(word,None) or pinyin.convert(word) for word in line]
        print ' '.join(words)
        
