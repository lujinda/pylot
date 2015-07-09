#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-07 13:55:18
# Filename      : index.py
# Description   : 
from handler.public import ApiHandler, authenticated
from db.brand import brand_name_is_exist, brand_alias_name_is_exist, add_brand, get_all_brand, update_brand, remove_brand
from mimetypes import guess_type

class BrandIndexHandler(ApiHandler):
    @authenticated
    def get(self):
        brands = get_all_brand()
        self.render('brand/index.html', brands = brands)

    @authenticated
    def post(self):
        """添加新的品牌时用得"""
        brand_name, brand_alias_name, brand_logo_url, brand_summary = self.get_true_args(
                'brand_name', 'brand_alias_name', 'brand_logo_url', 'brand_summary')
        if self.has_error():
            return
        add_brand(brand_name, brand_alias_name, brand_logo_url, brand_summary = brand_summary)

    @authenticated
    def put(self):
        brand_id, brand_name, brand_alias_name, brand_logo_url, brand_summary = self.get_true_args('brand_id',
                'brand_name', 'brand_alias_name', 'brand_logo_url', 'brand_summary')

        if self.has_error():
            return
        update_brand(brand_id, brand_name, brand_alias_name, brand_logo_url, brand_summary)

    def get_brand_name(self):
        brand_name = self.get_body_argument('brand_name', None)
        if not brand_name:
            self.set_error('品牌名字不能为空哦')
            return

        if self.is_update == False and brand_name_is_exist(brand_name):
            self.set_error(u'{brand_name} 已存在'.format(brand_name = brand_name))
            return 

        return brand_name

    def get_brand_alias_name(self):
        brand_alias_name = self.get_body_argument('brand_alias_name', None)
        if not brand_alias_name:
            self.set_error('品牌别名不能为空')
            return

        if not brand_alias_name.isalpha():
            self.set_error('品牌只允许为字母')
            return

        if self.is_update == False and brand_alias_name_is_exist(brand_alias_name):
            self.set_error('品牌别名 {brand_alias_name} 已经存在，请修改'.format(
                brand_alias_name = brand_alias_name))
            return

        return brand_alias_name

    def get_brand_logo_url(self):
        brand_logo_url = self.get_body_argument('brand_logo_url', None)
        if not brand_logo_url:
            return "品牌logo图片url不可为空"
        logo_name = brand_logo_url.split('/')[-1]
        mime_type = guess_type(logo_name)[0]
        if mime_type and mime_type.startswith('image'):
            return brand_logo_url
        else:
            self.set_error('logo必须是图片哦')
            return

    def get_brand_summary(self):
        brand_summary = self.get_body_argument('brand_summary', None)
        if brand_summary and len(brand_summary) > 500:
            self.set_error('品牌简介请在500字之间')
            return 
        return brand_summary

    def get_brand_id(self):
        return self.get_body_argument('brand_id', None)

    @property
    def is_update(self):
        return bool(self.get_brand_id())

    @authenticated
    def delete(self):
        remove_brand(self.get_brand_id())

