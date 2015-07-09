#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-08 19:21:23
# Filename      : model.py
# Description   : 
from handler.public import ApiHandler, authenticated
from tornado.web import HTTPError
from db.brand import brand_alias_name_is_exist, get_brand, model_name_is_exist, add_model, get_all_model, get_model_param, remove_model
from util.util import is_float

ALL_OS = {'ios': '苹果', 'android': '安卓'}
ALL_NETEWORK = {'GSM': '移动/联通2G', 'WCDMA': '联通3G', 'CDMA200': '电信3G', 'CDMA': '电信2G', 'TD-SCDMA': '移动3G', 'telecom_4g': '电信4G',
        'mobile_4g': '移动4G', 'unicom_4g': '联通4G', 'wifi': 'wifi'}

class BrandModelHandler(ApiHandler):
    @authenticated
    def get(self, brand):
        if 'model_id' in self.request.arguments: # 如果带有model_id参数，则表示是想要查看配置信息
            model_param = get_model_param(self.get_query_argument('model_id'))
            if not model_param:
                self.set_error('该型号不存在')
            else:
                self.process_model_param(model_param['param'])
                self._result_json.update(model_param)
            return

        brand_alias_name = brand
        if not brand_alias_name_is_exist(brand_alias_name):
            raise HTTPError(404)

        brand = get_brand(brand_alias_name = brand_alias_name)
        models = get_all_model(brand['id'])
        self.render('brand/model.html', brand = brand, models = models, all_os = ALL_OS, all_network = ALL_NETEWORK)

    def process_model_param(self, model_param):
        model_param['screen_size'] += u'寸'
        model_param['os'] = ALL_OS[model_param['os']]
        model_param['network'] = map(ALL_NETEWORK.get, model_param['network'])
        model_param['space_size'] = [x + 'G' for x in  model_param['space_size']]

    @authenticated
    def delete(self, brand):
        model_id = self.get_model_id()
        if self.has_error():
            return
        remove_model(model_id)

    def get_model_id(self):
        model_id = self.get_argument('model_id', None)
        if not model_id:
            self.set_error('型号id不可少')
            return
        return model_id

    @authenticated
    def post(self, brand):
        brand_alias_name = brand
        brand = get_brand(brand_alias_name = brand_alias_name)
        assert brand

        brand_id = brand['id']
        model_name, model_param = self.get_true_args('model_name', 'model_param')
        if self.has_error():
            return
        add_model(brand_id = brand_id, model_name = model_name,
                model_param = model_param)

    def get_model_name(self):
        model_name = self.get_body_argument('model_name', '').strip()
        if not model_name:
            self.set_error('型号名不能为空')

        if model_name_is_exist(model_name):
            self.set_error(u'%s 已存在' % (model_name))

        return model_name

    def get_model_param(self):
        param_list = ['screen_size', 'os', 'pixels', 'phone_from', 'color', 'space_size', 'network']
        param = dict(zip(
            param_list, self.get_true_args(*param_list)))

        return param

    def get_screen_size(self):
        screen_size= self.get_body_argument('screen_size', None)
        if not screen_size:
            self.set_error('屏幕尺寸不能为空')

        if not is_float(screen_size):
            self.set_error('屏幕尺寸必须是数字')

        return screen_size

    def get_os(self):
        os = self.get_body_argument('os', None)
        if not os:
            self.set_error('操作系统名称不能为空')

        if os not in ALL_OS.keys():
            self.set_error('操作系统名称不合法')

        return os

    def get_pixels(self):
        pixels = self.get_body_argument('pixels', '').strip()
        if not pixels:
            self.set_error('像素不能为空')
        
        if not pixels.isdigit():
            self.set_error('像素必须全是数字哦')

        return pixels

    def get_phone_from(self):
        """获取手机的源地，可能会有多个，所以需要加s"""
        phone_from = self.get_has_arguments('phone_from')
        if not phone_from:
            self.set_error('来源地不可为空')

        return phone_from

    def get_color(self):
        color = self.get_has_arguments('color')
        if not color:
            self.set_error('机身颜色不可为空')

        return color
    def get_space_size(self):
        space_size = self.get_has_arguments('space_size')
        if not space_size:
            self.set_error('存储容量大小不能为空')
            return False

        for _size in space_size:
            if not is_float(_size):
                self.set_error('容量必须是数字')

        return space_size

    def get_network(self):
        network = self.get_has_arguments('network')
        if not network:
            self.set_error('网络机制不可少')
            return 

        if bool(set(network) - set(ALL_NETEWORK.keys())):
            self.set_error('网络不合法')

        return network


