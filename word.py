#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-16 00:20:45
# Filename        : word.py
# Description     : 

import string
import re

class WordTop(object):
 #   word_list = []
    __word_count = {}
    __word_top = []
    def __init__(self, fd):
        self.__fd = fd
        self.made_word_list()
        self.pos = 0

    def made_word_list(self):
        re_string = map(lambda x:'\\' + x,
            string.punctuation)
        re_string.remove("\\'")
        re_string.append("'s")
        re_word = re.compile(r"%s" % 
                '|'.join(re_string))

        for line in self.__fd:
            line = re_word.sub(' ', line).lower()
            line_words = line.split()
            for word in line_words:
                self.__word_count[word] = self.__word_count.get(word,0) + 1
#            self.word_list.extend(line_words)

    
    def __top_n(self, n):
        for word in self.__word_count:
            end_word, end_count = self.get_end_max()
            count = self.__word_count[word]
            if count < end_count and n == len(self.__word_top):
                continue
            else:
                self.ord_list((word, count))
                if n < len(self.__word_top) and n:
                    self.__word_top.pop()

        return self.__word_top

    def ord_list(self,new_item):
        for i,item in enumerate(self.__word_top):
            if item[0] == new_item[0]:break
            if item[1] < new_item[1]:
                self.__word_top.insert(i, new_item)
                break
        else:
            self.__word_top.append(new_item)

    def get_end_max(self):
        if self.__word_top:
            return self.__word_top[-1]
        else:
            return '', 0

    def top_n(self, n = 0):
        if n > len(self.__word_top) or n == 0:
            print self.__top_n(n)
        else:
            print self.__word_top[:n]
        

