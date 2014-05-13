#coding:utf8
import sys,re
from handlers import *
from util import *
from rules import *

class Parser:
    def __init__(self,handler):
        self.handler=handler
        self.rules=[]
        self.filters=[]
    def addRule(self,rule):
        self.rules.append(rule)
    def addFilter(self,pattern,name):
        def filter(block,handler):
            return re.sub(pattern,handler.sub(name),block)
        self.filters.append(filter)
    def parse(self,file):
        self.handler.start("document")
        for block in blocks(file):
            for filter in self.filters:
                block=filter(block,self.handler) # 对过滤条件进行循环，把已经替换好的内容赋值给block 比如<a href....>
            for rule in self.rules: # 对规则进行判断，只判断一次就要退出,比如<title></title>
                if rule.condition(block):
                    if rule.action(block,self.handler):break

        self.handler.end("document")

class BasicTextParser(Parser):
    def __init__(self,handler):
        Parser.__init__(self,handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r"((http|ftp)://[\.\w\\]+)","url")
        self.addFilter(r"\*(.+?)\*","emphasis")
        self.addFilter(r"(\w+@[\w\.]+\w+)","mail")

handler=HTMLRenderer()
parser=BasicTextParser(handler)

parser.parse(sys.stdin)
