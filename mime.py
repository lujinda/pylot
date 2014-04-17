#!/usr/bin/env python

import sys,email
counter=0
parts=[]

def printmsg(msg,level=0):
    global counter
    l="| " *level
    ls=l + "*"
    l2=l + "|"
    if msg.is_multipart():
        print l+ "Found multipart:"
        for item in msg.get_payload():
            printmsg(item,level+1)
    else:
        disp=["%d.Decodable part" %(counter+1)]
        if "content-type" in msg:
            disp.append(msg["content-type"])
        if "content-disposition" in msg:
            disp.append(msg["content-disposition"])
        print l + ", ".join(disp)
        counter +=1
        parts.append(msg)

inputfd=open("mail.list")
msg=email.message_from_file(inputfd)
printmsg(msg)

while 1:
    part=raw_input()
    if part=="quit":
        sys.exit(0)
    try:
        part=int(part)
        msg=parts[part-1]
    except:
        print "Invalid selection"
        continue

    try:
        fd=open(raw_input("Select file to write to:"),"wb")
    except:
        print "Invalid filename."
        continue
    message=msg.get_payload(decode=1)
    message=unicode(message,msg.get_content_charset()).encode("utf8") if msg.get_content_charset() else message
    fd.write(message)
