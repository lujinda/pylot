import os
import sys

def listDir(path,level=0):
    for item in os.listdir(path):
        if os.path.isdir(path+'/'+item):
            print '+',item
            listDir(path+'/'+item,level+1)
        else:
            print '| '*level+item
        

listDir(".")
