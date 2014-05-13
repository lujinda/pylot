#coding:utf8
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import sys

def indent(elem,level=0):
    i="\n"+level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text=i+"\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail=i
        for elem in elem:
            indent(elem,level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail=i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail=i

def createElem():
    contact=ET.Element("contact")
    name=ET.SubElement(contact,"Name")
    name.text=raw_input("请输入名字:").decode("utf8")
    phoneList=ET.Element("PhoneList")
    for num in raw_input("请输入号码，多个号码间以空格相隔:").split():
        phone=ET.SubElement(phoneList,"Phone")
        phone.text=num
        phone.set("Type","2")
    return ((contact,phoneList))
    
root=ET.Element("Contacts")
for i in range(1):
    root.extend(createElem())
indent(root)
xml_string=ET.tostring(root)
print xml_string

