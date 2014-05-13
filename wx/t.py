#coding:utf8
import xml.etree.ElementTree as et
import sys
import os

def cDirItem(name):
    currdir=et.Element("directory")
    currdir.set("name",name)
    return currdir

def indent(elem,level=0):
    i='\n'+level*'\t'
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text=i+'\t'
            elem.tail=i
        for elem in elem:
            indent(elem,level+1)
        elem.tail=i
    else:
        if level:
            elem.tail=i

def createElem(path):
    fileitem=et.Element("file")
    for tag,value in zip(("path","size"),
            (path,os.path.getsize(path))):
        fileitem.set(tag,str(value).decode("utf8"))
        fileitem.text=os.path.basename(path).decode("utf8")
    return ((fileitem,))

def createElems(path="."):
    global root
    for name in os.listdir(path):
        p=os.path.join(path,name)
        if not os.path.isdir(p):
            root.extend(createElem(p))
        else:
            createElems(p)
    
if __name__=="__main__":
    root=et.Element("filelist")
    createElems()
    indent(root)
    tree=et.ElementTree(root)
    tree.write(sys.stdout,"utf-8",True)
