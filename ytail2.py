import time
def tail(fd):
    fd.seek(0,2)
    while True:
        line=fd.readline()
        if not line:
            time.sleep(0.1)
            continue
        print 'tail yield befor'
        yield line #会在这阻塞

def grep(lines,searchtext):
    for line in lines:
        if searchtext in line:
            print 'grep yield befor'
            yield line # 会在这里阻塞，然后进行上面的那个yield

flog=tail(open("/var/log/apache2/access.log",'r'))
pyline=grep(flog,'127.0.0.1')
for line in pyline:
    print line,
