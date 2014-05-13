import os
import itertools

def anyTrue(fun,seq):
    return True in itertools.imap(fun,seq)

def endsWith(filename,*args):
    return anyTrue(filename.endswith,args)

for filename in os.listdir("."):
    if endsWith(filename,".pyc",".txt"):
        print filename
