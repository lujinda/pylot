#!/usr/bin/env python
#coding:utf8
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.Encoders import encode_base64

import email
import mimetypes
import sys
import re
import smtplib
import os
import time

Path=os.path.dirname(os.path.abspath(sys.argv[0]))

userInfo={
        "username":None,
        "password":None,
        "host":None,
        }

def addFile():
    try:
        mainType,subType=mimetypes.guess_type(filename)[0].split('/')
    except:
        mainType="application"
        subType="None"
    fd=open(filename,"rb")
    if mainType=="text":
        msgAttr=MIMEText(fd.read())
    #elif mainType=="image":
     #   msgAttr=MIMEImage(fd.read(),_subtype=subType)
   # elif mainType=="audio":
    #    msgAttr=MIMEAudio(fd.read(),_subtype=subType)
    else:
        msgAttr=MIMEBase(mainType,subType)
        msgAttr.set_payload(fd.read())
        encode_base64(msgAttr)
    msgAttr["Content-Disposition"]="attachment;filename=%s" %unicode(os.path.basename(filename),"utf8").encode("gbk")
    fd.close()
    return msgAttr

def sendMail(smtp):
    msgRoot=MIMEMultipart()
    msgRoot["Subject"]=u"%s:%s" %(time.strftime("%Y-%m-%d %T"),unicode(os.path.basename(filename),"utf8"))
    fromTo=userInfo["username"]
    msgRoot["From"]=fromTo
    msgRoot["To"]=';'.join(to_list)
    msgRoot.attach(addFile())
    smtp.sendmail(fromTo,to_list,msgRoot.as_string())

def readInfo():
    try:
        fd=open(os.path.join(Path,"sendmail.conf"),"r")
        lines=fd.readlines()
        for line in lines:
            key,value=re.findall("(.+?)\s*=\s*([^\s].+)",line)[0]
            userInfo[key]=value
    except:
        print "read info error!"
        sys.exit(1)
    finally:
        fd.close()
            
def login(username,password,host):
    try:
        smtp=smtplib.SMTP()
        smtp.connect(host)
        smtp.login(username,password)
        return smtp
    except Exception,e:
        print e
        sys.exit(2)

try:
    filename=sys.argv[1]
    to_list=sys.argv[2:]
except Exception,e:
    print e
    print "format:filename + to_list"
    sys.exit(3)
readInfo()
smtp=login(**userInfo)
smtp.ehlo()
maxSize=smtp.esmtp_features.get("size")
if maxSize and maxSize < os.path.getsize(filename):
    print 'over maxsize!'
    sys.exit(10)
else:
    sendMail(smtp)
