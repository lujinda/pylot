import sys,os
def daemonize(stdin="/dev/null",stdout="/dev/null",stderr="/dev/null"):
    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)
    except OSError,e:
        sys.stderr.write("Fork failed\n")
        sys.exit(1)

    os.umask(0)
    os.setsid()

    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)
    except OSError,e:
        sys.stderr.write("Fork failed\n")
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    si=open(stdin,'r')
    so=open(stdout,'a+')
    se=open(stderr,'a+')

    os.dup2(si.fileno(),sys.stdin.fileno())
    os.dup2(so.fileno(),sys.stdout.fileno())
    os.dup2(se.fileno(),sys.stderr.fileno())

