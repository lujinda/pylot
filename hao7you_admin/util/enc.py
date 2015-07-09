#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-06 16:42:39
# Filename      : env.py
# Description   : 
import hashlib

def change_char(char):
    assert 0 < ord(char) <= 128
    if char.isdigit():
        return str(9 - int(char))
    
    if char.islower():
        return chr(ord(char) - 32)

    if char.isupper():
        return chr(ord(char) + 32)

def enc_password(password):
    password = ''.join(map(change_char, password)) # 先对密码的字符串做一个简单的加密
    salt_password = ".#$abc" + password + 'wx\)'
    m = hashlib.md5(salt_password)
    return m.hexdigest()

