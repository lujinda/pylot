#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-03 22:50:13
# Filename        : weixin.py
# Description     : 
from config import render,kv_db,get_isLoginOk
import os
import urllib2,json
import lxml
from lxml import etree
import time
import hashlib
import web



__all__ = ["WeixinInterface"]


        
class obj_pc():
    def __init__(self,line,fromUser):
        self.line = line
        self.fromUser = fromUser
        
    def do_pc(self):
    	kv_db.set(self.fromUser + "_where", "pc_content")  # 改动当前位置，使用kd来判断当前位置
    
        return u'请输入您遇到的电脑问题，至少要10个字哦～暂时不支持加图片。回复"#"退出故障提交模式'    
  
    def do_pc_content(self):
    	from submit import check_content
        
        if check_content(self.line):
            kv_db.set(self.fromUser + "_where", "pc_name")
            kv_db.set(self.fromUser + "_content", self.line)
        else:
            return u"您输入的故障信息不能少于10个字哦～～请重新输入"
        return u"请输入您的名字"    
    
    def do_pc_name(self):
        from submit import check_name
        if check_name(self.line):
            kv_db.set(self.fromUser + "_where", "pc_phone")
            kv_db.set(self.fromUser + "_name", self.line)
        else:
            return u"您输入的姓名不要太长，或太短哦"
        return u"请输入您的联系方式"
        
    
    def do_pc_phone(self):
        from submit import check_phone
        
        if check_phone(self.line):
            kv_db.set(self.fromUser + "_where", "pc_room")
            kv_db.set(self.fromUser + "_phone", self.line)
        else:
            return u"您输入的联系方式错误，请输入11位长号，或6位长号"
       # return self.__do_pc_data() # 到这信息都输入完毕，确定提交了
        return u"您的寝室号？"
        
    def do_pc_room(self):
        kv_db.set(self.fromUser + "_where", "pc_when")
        kv_db.set(self.fromUser + "_room", self.line)
        
        return u"希望我们什么时候过去修？或者说你什么时候有空？"
    
    def do_pc_when(self):
        kv_db.set(self.fromUser + "_where", "pc_end")  # 定位
        kv_db.set(self.fromUser + "_when", self.line)  # 存值
        
        return self.__do_pc_data() # 到这信息都输入完毕，确定提交了
            
    
    def do_pc_end(self):
        if self.line.lower() != 'y':
            self.__do_clear()
            return  u"取消提交"
        else:
            if self.__do_pc_submit():
                self.__do_clear()
                return u"提交成功"
            else:
                return u"提交失败，是否重试?"
    

    
    def __do_pc_data(self):  # 对提交问题的最后一个确定
        data = [
                u"故障: " + kv_db.get(self.fromUser + "_content"),
                u"姓名: " + kv_db.get(self.fromUser + "_name"),
                u"联系方式: " + kv_db.get(self.fromUser + "_phone"),
                u"寝室号: " + kv_db.get(self.fromUser + "_room"),
                u"维修时间: " + kv_db.get(self.fromUser + "_when"),
                u"确定提交(回复'y'表示确定)？",
                ]
        return '\n'.join(data)
    
    
    
    
            
    def __do_pc_submit(self):
        class Data():  # 为了和writeDb接口匹配
            Content = kv_db.get(self.fromUser + "_content")
            Name = kv_db.get(self.fromUser + "_name")
            Phone = kv_db.get(self.fromUser + "_phone")
            Room = kv_db.get(self.fromUser + "_room")
            Time = kv_db.get(self.fromUser + "_when")

        from submit import sendSubmit
        data = Data()
        try:
            sendSubmit().writeDb(data)
            return True
        except:
            return False
        
    #...................................................................
    
class obj_search():
    def __init__(self,line,fromUser):
        self.line = line
        self.fromUser = fromUser
        
    #下面是关于搜索的.....................................................
    def do_search(self):
        kv_db.set(self.fromUser + "_where", "search_content")  # 改动当前位置，使用kd来判断当前位置
        return u'请输入您的故障,2～30字\n(尽可以输得简单直白一点，不要拖泥带水。\
        <a href="http://ljdpython.sinaapp.com/help#search">使用帮助</a>)\n回复"#"退出搜索模式'
    
    def do_search_content(self):
        if not (2 <= len(self.line) <= 30):
            return u"问题字数请控制在2～30"
        else:
            request = [u"问题: %s" % self.line,
                       u'答案: <a href="http://ljdpython.sinaapp.com/sendKw?Kw=%s">点击查看</a>' % self.line,
                       u'回复"#"退出搜索模式',
                      ]
            return '\n'.join(request)

    #....................................................................... 
        
    

class CommandHandler:
    def handle(self, line, fromUser):
        #self.fromUser = fromUser
     
        cmd_list={ # 数字指令与文字指令对应的函数
            u'1':"list", u'技术人员':"list",
            u'2':"mess", u'最新公告':"mess",
            u'3':"pc", u'电脑报修':"pc",
            u'4':"search", u'搜索问题':"search",
        #    u'bug':"bug",
            u'#':"help",
                }
        in_where = kv_db.get(self.fromUser + "_where") # 获取当前所在位置。如果是首页，则是None
        
        if in_where and line.strip() != '#':  # 如果不在首页，则以当前所在位置，调用相应的函数。函数名是do_当前位置。
           # self.line = line
            command = in_where

        else:
            command = cmd_list.get(line.strip(),'help')  # 如果指令不存在，则使用help，只在首页有效果
        
        return u"command"
        
        if command.startswith("pc_"):
            obj = obj_pc(line,fromUser)
        elif command.startswith("search_"):
            obj = obj_search()
        else:
            obj = self
        
        
        func = getattr(obj, 'do_' + command, None)
        try:
            request = func()
        except TypeError:
            request = self.do_help()

        return request
   	

    def do_list(self):
        from config import get_listDb
        listDb = map(lambda x: ' '.join(x[1:]), get_listDb())
        return "\n".join(listDb)
        
    
    def do_mess(self):
        from config import get_mess
        mess = get_mess()
        return mess
    

    

 
    
    def __do_clear(self):
        in_where = kv_db.get(self.fromUser + "_where")
        if not in_where:  # 如果当前在首页，则不需要清除相应记录
            return None
        if in_where.startswith("pc_"): # 在故障报修下的子菜单，就只清理下面的东西就行
            kd_list = ["_content","_name","_phone","_where","_room","_when"]
        if in_where.startswith("search_"):
            kd_list = ["_where"]  # 如果在搜索模式下，就只有清空当前位置信息，返回首页就行。
          
        
        for item in kd_list:
            kv_db.delete(self.fromUser + item)

    def do_help(self):
    	self.__do_clear()
        help_mess=[
                u'***输入以下指令前的"编号"可获取协会的相关信息***',
                u'"1.技术人员"——获取技术人员联系方式',
                u'"2.最新公告"——获取协会的最近活动信息',
                u'"3.电脑报修"——电脑出问题了？把问题提交给我们吧',
                u'"4.搜索问题"——来我们的已解决故障的数据库中查找答案吧',
                u'"#.返回到首页"'
                ]
        return '\n'.join(help_mess)
    
    
    


class WeixinInterface:
    def __init__(self):
        self.handler=CommandHandler()

    def GET(self):
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="e0148a97a6c42b3d283cc2c5041260b9"
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        
 
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):        
        str_xml = web.data() 
        xml = etree.fromstring(str_xml)
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        
        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                content = u"#"
 
        if msgType == "text":
            content = xml.find("Content").text# 当msgType是event是无法找到Content的，所以这行代码，不能放在前面，要不会500
        return render.reply_text(fromUser,toUser,int(time.time()),u"%s"%self.handler.handle(content,fromUser))




