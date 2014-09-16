#coding:utf8
from threading import Thread
import threading
import time
import random
from Queue import Queue

class Producer(Thread):
    def run(self):
        global queue
        count=0
        while True:
            for i in range(100):
                if queue.qsize()>100:
                    pass
                else:
                    r.acquire()
                    count+=1
                    msg='生成产品'+str(count)+'当前产品有'+str(queue.qsize())
                    queue.put(msg)
                    print msg
                    r.release()

            time.sleep(1)


class Consumer(Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize()<100:
                pass
            else:
                m=self.name+"消费了"+queue.get(block=True)
                print m

            time.sleep(1)

r=threading.RLock()
queue=Queue()
for i in range(2):
    p=Producer()
    p.start()
for i in range(50):
    c=Consumer()
    c.start()
