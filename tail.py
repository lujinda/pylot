import time
def grep(line,searchtext):
    if searchtext in line:
        print line,
    
def tail(fd):
    fd.seek(0,2)
    while True:
        line=fd.readline()
        if not line:
            time.sleep(0.1)
            continue
        grep(line,'127.0.0.1')
flog=tail(open("/var/log/apache2/access.log",'r'))

