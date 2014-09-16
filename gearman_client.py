#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-08-29 11:52:16
# Filename        : gearman_client.py
# Description     : 
from gearman import GearmanClient

new_client=GearmanClient(["192.168.8.116:1234"])
fd=open("亮剑.txt",'r')
line=fd.readline()
request=new_client.submit_job('pinyin',line)
print dir(request)

