#coding:utf8
import time
import urllib2
import threading
from Queue import Queue
from time import sleep

PERF_TEST_URL="http://ljdpython.sinaapp.com/frame/main.html"

THREAD_NUM=100
ONE_WORKEN_NUM=100
LOOP_SLEEP=0.5

ERROR_NUM=0

def doWork(index):
    t=threading.currentThread()
    try:
        html=urllib2.urlopen(PERF_TEST_URL).read()
    except urllib2.URLError,e:
        print "["+t.name+" "+str(index)+"] "
        print e
        global ERROR_NUM
        ERROR_NUM+=1


def working():
    t=threading.currentThread()
    print "["+t.name+"] Sub Thread Begin"

    i=0
    while i<ONE_WORKEN_NUM:
        i+=1
        doWork(i)
        sleep(LOOP_SLEEP)

def main():
    t1=time.time()
    Threads=[]
    for i in range(THREAD_NUM):
        t=threading.Thread(target=working,name="T"+str(i))
        t.setDaemon(True)
        Threads.append(t)

    for t in Threads:
        t.start()

    for t in Threads:
        t.join()

    print "main thread end"

    t2=time.time()
    print "==============================="
    print "URL:",PERF_TEST_URL
    print "任务数量:",THREAD_NUM,'*',ONE_WORKEN_NUM,"=",THREAD_NUM*ONE_WORKEN_NUM
    print "总耗时(秒):",t2-t1
    print "每次请求耗时(秒):",(t2-t1)/(THREAD_NUM*ONE_WORKEN_NUM)
    print "每秒承载请求数：",1/((t2-t1)/(THREAD_NUM*ONE_WORKEN_NUM))
    print "错误数量:",ERROR_NUM

if __name__=="__main__":
    main()
