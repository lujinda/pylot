import time
import datetime
import shelve
import optparse

def parse_args():
    usage="usage: %prog [set]"
    parser=optparse.OptionParser(usage)
    
    _,option=parser.parse_args()

    if not option:
        return "show"
    
    if option[0]!='set':
        return "show"
    return "set"

DB_PATH="/home/ljd/py/.date.db"

class commandHandler():
    def handler(self,line):
        parts=line.split(' ',1)
        cmd=parts[0]
        try:
            line=parts[1]
        except IndexError:
            line=""
        
        func=getattr(self,"do_"+line,None)
        try:
            func(line)
        except TypeError:
            self.do_help()

    def do_help(self):
        pass
        
class countDown(commandHandler):
    def __init__(self):
        self.database=shelve.open(DB_PATH,c)

    def do_show(self,line):
        pass

    def do_end(self,line):
        self.database.close()

class showData(countDown):
    pass

class setData(countDown):
    def do_set(self,line):
        pass
    
    def do_del(self,line):
        pass
    
    def do_delall(self,line):
        pass

    def do_add(self,line):
        pass

def main():
    action=parse_args()
    if action=="show":
        do=showData
    else:
        do=setData
    print do
    

if __name__=="__main__":
    main()
        
