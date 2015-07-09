#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-30 09:34:19
# Filename      : __init__.py
# Description   : 
import os
IGNORE_MODULE = ['public', 'base']
MY_DIR = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在的路径，为了做遍历整个Handler
offset = len(MY_DIR) + 1

for root, dirs, files in os.walk(MY_DIR): 
    for _file in files:
        if (not _file.endswith('.py')) or (_file.startswith('_')): # 只对python文件做遍历
            continue
        file_path = os.path.join(root, _file)
        if file_path in IGNORE_MODULE:
            continue
        module_path = file_path[offset:].replace('/', '.')[:-3]

        p = __import__('handler.%s' % (module_path), 
                fromlist = [module_path, ])
    
        for attr in dir(p):
            if attr.endswith('Handler'):
                exec('from handler.%s import %s' % (module_path, 
                    attr))

handlers = [
        ('/', IndexHandler),
        ('/login', LoginHandler),
        ('/logout', LogoutHandler),
        ('/active', AccountActiveHandler),
        ('/tag', TagIndexHandler),
        ('/brand/?', BrandIndexHandler),
        ('/brand/(\w+)', BrandModelHandler),
        ('/manager/(\w+)', ManagerHandler),
        ]

