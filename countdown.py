#!/usr/bin/env python
#coding:utf8
import time
import datetime
import shelve
import sys
import re
import optparse
import logging

log_file="/var/log/countdown.log"

def parse_args():
    usage="usage: %prog [set]"
    parser=optparse.OptionParser(usage)
    
    _,option=parser.parse_args()

    if not option:
        return "show"
    
    if option[0]!='set':
        return "show"
    return "set"

DB_PATH="/home/ljd/py/data.db"

class commandHandler():
    def handler(self,line):
        parts=line.split(' ',1)
        cmd=parts[0]
        try:
            line=parts[1]
        except IndexError:
            line=""
        
        func=getattr(self,"do_"+cmd,None)
        try:
            func(line)
        except TypeError,e:
            self.do_help(cmd)

    def do_help(self,cmd):
        print """command list:
        show
        set <序号>
        end
        del <序号>
        add <事件名:事件要发生的日期>
        delall"""
        
class countDown(commandHandler):
    def __init__(self):
        self.__conflog()
        
        self.re_thing=re.compile(r"\"(.+?)\"")
        self.database=shelve.open(DB_PATH,'c')
        self.handler("show")

    def __conflog(self):
        self.logger=logging.getLogger("countDown")
        handler=logging.FileHandler(log_file)
        formatter=logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def do_show(self,line):
        self.listItem={}
        things=[self.toTime(x,y) for x,y in self.database.items()]
        for i,thing in enumerate(things):
            print "(%d) %s "%(i+1,thing)
            self.listItem[str(i+1)]=self.re_thing.findall(thing)[0]

    def toTime(self,thing,time):
        date=datetime.datetime(*map(int,time.split('-')))
        nowDate=datetime.datetime.now()
        dates=(date-nowDate).days + 1

        if dates>=0:
            line="离\"%s\"还有 %d 天"%(thing,dates)
        else:
            line="\"%s\"已经过去了 %d 天"%(thing,abs(dates))
        return line

    def do_end(self,line):
        self.database.close()
        sys.exit(0)

class showData(countDown):
    def __init__(self):
        countDown.__init__(self)
        self.handler("end")

class setData(countDown):
    def __init__(self):
        countDown.__init__(self)
        self.input_do()

    def input_do(self):
        while 1:
            try:
                line=raw_input("> ")
            except KeyboardInterrupt:
                self.handler("end")
            self.handler(line.strip())

    def do_set(self,line):
        thing=self.getKey(line)
        if thing:
            newDate=raw_input("请输入新日期(year-mon-day):")
            
            self.handler("add %s:%s"%(thing,newDate))
            
    def do_add(self,line):
        try:
            thing,date=line.split(':',1)
            try:
                self.toTime(" ",date)   # 起到测试日期是否合理作用
            except:
                print "请输入正确日期!"
                return None
            
            self.database[thing]=date
            self.logger.info("%s >> %s"%(thing,date))
            self.handler("show")
        except (KeyError,ValueError):
            print "请正确输入(事件名:事件发生日期):"
            return None
            
    def getKey(self,line):
        try:
            return self.listItem[line]
        except KeyError:
            print "请选择一个有效的序列!"
            return None
        
    
    def do_del(self,line):
        try:
            thing=self.getKey(line)
            time=self.database[thing]
            del self.database[thing]
            self.logger.info("del %s at %s"%(thing,time))
            self.handler("show")
        except:
            pass

    def do_delall(self,line):
        self.database.clear()
        self.logger.info("del all things")

def main():
    action=parse_args()
    if action=="show":
        do=showData()
    else:
        do=setData()


if __name__=="__main__":
    main()
        
