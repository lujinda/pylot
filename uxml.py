import xml.etree.ElementTree as et
import sys
import os
from xml.dom import minidom
from itertools import izip
import time

IMGPATH="/home/ljd/Dropbox/img/"
def make_starttime(root):
    starttime=et.SubElement(root,"starttime")
    for x,y in izip(("year","month","day","hour","minute","second"),
            time.strftime("%Y %M %d %H %m %S").split()):
        et.SubElement(starttime,x).text=y

def make_img(root):
    nameData=os.listdir(IMGPATH)
    Last=nameData[-1]
    for name in nameData[0:]:
        Next=name
        static=et.SubElement(root,"static")
        et.SubElement(static,"duration").text="595.0"
        et.SubElement(static,"file").text=os.path.abspath(Last)
        transition=et.SubElement(root,"transition")
        et.SubElement(transition,"duration").text="5.0"
        et.SubElement(transition,"from").text=os.path.abspath(Last)
        et.SubElement(transition,"to").text=os.path.abspath(Next)
        Last=Next
    

root=et.Element("background")
make_starttime(root)
make_img(root)
tree=et.ElementTree(root)
tree.write("u.xml")
