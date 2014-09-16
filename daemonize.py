#!/usr/bin/env python
import sys,os
def daemonize(stdin="/dev/null",stdout="/dev/null",stderr="/dev/null"):
    try:
        pid=os.fork()  # 父进程和子进程都会执行一次，子进程中返回0,父进程中返回子进程的id
        if pid>0:
            sys.exit(0) # 退出了父进程。
    except OSError,e:
        sys.stderr.write("Fork 1# failed\n")
        sys.exit(1)

    os.chdir('/') # 切换到/目标，这样的话假如有目录需要消除挂载，就不会有影响了（python unix和unix系统管理指南中有这样写）
    os.umask(0) # 创建的文件将有完全权限
    os.setsid() # *如果不执行这个，则child和parent会在同一个session中，如果是从bash中启动程序的，则bash是这个session的领头进程。可以通过os.getsid(PID)查看
    try:
        pid=os.fork()  # 这个不是必要的了
        if pid>0:
            sys.exit(0)
    except OSError,e:
        sys.stderr,write("Fork 2# failed\n")
        sys.exit(1)

    sys.stdout.flush()  # 对标准输入标准错误做个清空操作
    sys.stderr.flush()

    si=open(stdin,'r')
    so=open(stdout,'a+')
    se=open(stderr,'a+')
    
    os.dup2(si.fileno(),sys.stdin.fileno())
    os.dup2(so.fileno(),sys.stdout.fileno())
    os.dup2(se.fileno(),sys.stderr.fileno())
    # 上述三个操作，是将标准输入，输出，错误重定向到三个文件中
