#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-28 16:03:05
# Filename        : gearman_worker.py
# Description     : 
import gearman
import sys
import re

TXTPATH="./utf-8.txt"
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
                if not re_zh.search(zh):
                    zh=yield zh
                    cache_word[zh]=zh
            yield None
        except OSError,e:
            sys.exit(1)
        finally:
            words.close()
            yield

    def task_callback(self,gearman_worker,job):
        if not job.data:return ''
        line=job.data.decode("utf8")
        print line
        words=[cache_word.get(word,None) or self.convert(word) for word in line]
        
        return ' '.join(words).encode("utf8")


pinyin=ToPinYin()

new_worker=gearman.GearmanWorker(["192.168.8.116:1234"])
new_worker.register_task("pinyin",pinyin.task_callback)
new_worker.work()


