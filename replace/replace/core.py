#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-19 14:04:03
# Filename      : core.py
# Description   : 
from __future__ import unicode_literals, print_function
import os
from replace.filefilter import FileFilter
import re

class FilesManager(object):
    def __init__(self, target_path = None, filter_filename= None, is_filter = True, 
            source_re_string = None, target_string = None,
            include_hidden = False):
        self.target_path = target_path or os.getcwd() # 如果没有指定路径，则是自己当前工作路径
        self.file_filter = FileFilter(filter_filename = filter_filename, 
                is_filter = is_filter, include_hidden = include_hidden)
        self.source_re_string = source_re_string
        self.target_string = target_string

    def list_all_files(self):
        if os.path.isfile(self.target_path): # 如果目标是个文件，则直接返回
            yield self.target_path

        for root, dirs, files in os.walk(self.target_path):
            for _file in files:
                _file = os.path.join(root, _file)
                if not self.file_filter.file_is_filter(_file):
                    yield os.path.join(root, _file)

    def all_replace(self, source_re_string = None, target_string = None):
        source_re_string = source_re_string or self.source_re_string
        target_string = target_string  or self.target_string

        assert source_re_string != None and target_string != None

        source_re = self.__compile_re(source_re_string)

        for _file in self.list_all_files():
            self.__replace_file(_file, source_re, target_string)

    def __compile_re(self, re_string):
        return re.compile(re_string)

    def __replace_file(self, _file, 
            source_re, target_string):
        _source_fd = open(_file, 'rb')
        _tmp_filename = get_tmp_filename(_file)
         # _tmp_fd = open(_tmp_filename, 'wb')

        for _line in _source_fd:
            print(source_re.sub(target_string, _line)) # 先把文件写到一个缓存临时文件中去

