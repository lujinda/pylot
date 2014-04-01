import time
def tail(f):
    f.seek(0,2)
    while True:
        line=f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
def grep(line,searchtext):
    while True:
        l=line.next()
        if searchtext in l:
            yield l
flog=tail(open('/var/log/apache2/access.log','r'))
pylines=grep(flog,'127.0.0.1')
for line in pylines:
    print line,

