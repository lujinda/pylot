import os
import sys

def listDir(currPath,level=0):
    for item in os.listdir(currPath):
        if os.path.isdir(item):
            print '+ ',item
            listDir(item,level+1)
        else:
            print '| '*level+item

listDir(".")
