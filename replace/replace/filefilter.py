#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-19 14:26:45
# Filename      : filefilter.py
# Description   : 
from __future__ import unicode_literals, print_function
import os
import glob

class FileFilter(object):
    def __init__(self, filter_filename = None, is_filter = True, include_hidden = False):
        self.filter_filename = filter_filename or []
        self.is_filter = is_filter # 如果is_filter是Flase，则表示只列出仅满足条件的
        self.filters = self.made_filters()
        self.include_hidden = include_hidden

    def made_filters(self):
        _filters = {}
        _filters['name'] = self.__name_is_filter

        return _filters

    def __name_is_filter(self, filename):
        if b'/' in filename: # 如果传入的不是文件名，而是个路径的话，则帮它换成文件名
            filename = os.path.basename(filename)

        for _match_str in self.filter_filename:
            if glob.fnmatch.fnmatch(filename, _match_str):
                return True

        return False

    def file_is_filter(self, target_file, filter_type = 'name'):
        if not self.include_hidden: # 控制隐藏文件是否要过滤掉
            if glob.fnmatch.fnmatch(os.path.basename(target_file), '.*'):
                return True

        _filter = self.filters.get(filter_type)
        assert _filter, 'filter_type error'

        _is_filter = _filter(target_file)
        if self.is_filter:
            return _is_filter
        else:
            return not _is_filter

