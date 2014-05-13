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
            elem.tail=i
        for elem in elem:
            indent(elem,level+1)
        elem.tail=i
    else:
        if level:
            elem.tail=i

def createElem():
    contact=ET.Element("Contact")
    for s in ("Name","Starred"):
        elem=ET.SubElement(contact,s)
        elem.text="0" if s[0]=="S" else raw_input("请输入名字:").decode("utf8")
        if not elem.text.strip():raise Exception
    phoneList=ET.SubElement(contact,"PhoneList")
    for num in raw_input("请输入号码，多个号码间以空格相隔:").split():
        phone=ET.SubElement(phoneList,"Phone")
        phone.text=num
        phone.set("Type","2")
    account=ET.SubElement(contact,"Account")
    account.set("value","0")
    for tag,text in zip(("Name","Type"),("default","com.android.contacts.default")):
        ET.SubElement(account,tag).text=text

    return ((contact,))
    
root=ET.Element("Contacts")
while True:
    try:
        root.extend(createElem())
    except:
        break
indent(root)
tree=ET.ElementTree(root)
tree.write("t.xml","utf-8",True) # 第三个参数如果指定，则会在xml文件最开始，加上一个信息,比如编码

