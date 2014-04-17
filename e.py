import email
import sys
import poplib
import getpass
from email.Header import Header

host="pop.qq.com"
user="q8886888@qq.com"
pwd=getpass.getpass()

counter=0
parts=[]
def printmsg(msg):
    global counter
    if msg.is_multipart():
        for item in msg.get_payload():
            printmsg(item)
    else:
        disp=["%d"%(counter+1)]
        if "content-type" in msg:
            disp.append(msg["content-type"])
        if "content-disposition" in msg:
            disp.append(msg["content-disposition"])
        print ", ".join(disp)
        counter+=1
        parts.append(msg)
        

def login():
    try:
        p=poplib.POP3(host)
        p.user(user)
        p.pass_(pwd)
    except Exception,e:
        print "Login faile!",e
        sys.exit(1)
    return p

p=login()
lines=p.retr(p.stat()[0])[1]

msg=email.message_from_string('\n'.join(lines))
headers=email.header.decode_header(msg.get("subject"))
if headers:
    subject=unicode(headers[0][0],headers[0][1]).encode("utf8")
    print "Subject:%s"%subject

printmsg(msg)
while 1:
    c=raw_input("please select file:")
    if c=="quit":sys.exit(0)
    try:
        c=int(c)
        msg=parts[c-1]
    except Exception,e:
        print e
        continue
    try:
        filename=raw_input("Please input filename:")
        fd=open(filename,"wb")
        content=msg.get_payload(decode=1)
        if msg.get_content_type().split('/')[0] == "text":
            content=unicode(msg.get_payload(decode=1),
                    msg.get_content_charset()).encode("utf8")
        else:
            pass
            
        fd.write(content)
    except Exception,e:
        print e
        continue
fd.close()

