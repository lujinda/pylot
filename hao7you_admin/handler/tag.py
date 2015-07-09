#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-09 16:59:24
# Filename      : tag.py
# Description   : 
from .public import ApiHandler, authenticated
from db.tag import add_tag, tag_is_exist, get_all_tag, remove_tag, update_tag

class TagIndexHandler(ApiHandler):
    @authenticated
    def get(self):
        tags = get_all_tag()
        self.render('tag.html', tags = tags)

    def post(self):
        tag_name = self.get_tag_name()
        if self.has_error():
            return
        add_tag(tag_name)

    def put(self):
        tag_id, tag_name = self.get_true_args('tag_id', 'tag_name')
        if self.has_error():
            return
        update_tag(tag_id, tag_name)

    def delete(self):
        tag_id = self.get_tag_id()
        if self.has_error():
            return
        remove_tag(tag_id)

    def get_tag_name(self):
        tag_name = self.get_argument('tag_name', '').strip()
        if not tag_name:
            self.set_error('标签名不可为空')
            return 
        if (not self.get_tag_id()) and tag_is_exist(tag_name):
            self.set_error(u'%s 已存在' % (tag_name, ))
            return

        return tag_name

    def get_tag_id(self):
        tag_id = self.get_argument('tag_id', '').strip()
        return tag_id

