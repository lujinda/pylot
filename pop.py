#!/usr/bin/env python
import getpass
import poplib
import sys
import email

def log(text):
    sys.stdout.write(text)
    sys.stdout.flush()

host="pop.126.com"
user="ljd31415926@126.com"
passwd=getpass.getpass()

destfd=open("/tmp/mail.eml","wb")

log("Connecting to %s...\n"%host)
p=poplib.POP3(host)
try:
    log("Logging on...")
    p.user(user)
    p.pass_(passwd)
    log(" success.\n")
    
except:
    print "Login failed:",e
    sys.exit(1)

log("Scanning INBOX...")
mblist=p.list()[1]
log("have %d messages.\n" %len(mblist))

for item in mblist:
    number,octets=item.split(" ")
    log("Downloading message %s (%s bytes)...\n" %(number,octets))
    lines=p.retr(number)[1]
    msg=email.message_from_string('\n'.join(lines))
    destfd.write(msg.as_string(unixfrom=1))
    destfd.write("\n")

destfd.close()

p.dele(p.stat()[0])
log("Closing cocnnection...\n")
p.quit()
log("done\n")

    
