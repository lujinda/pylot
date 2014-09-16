import sys
try:
    cmd=sys.argv[1:]
except IndexError:
    print "need cmd!"
    sys.exit(1)

import xmlrpclib
server=xmlrpclib.ServerProxy("http://172.16.0.7:1234")
try:
    print server.do(cmd)
except Exception,e:
    print e
    sys.exit(0)
